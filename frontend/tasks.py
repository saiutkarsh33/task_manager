import streamlit as st
import requests
import threading
import time
import json
from sseclient import SSEClient  # pip install sseclient

API_URL = "http://localhost:8000"

# We’ll store received notifications in session state so they're persisted across re-runs.
if "notifications" not in st.session_state:
    st.session_state["notifications"] = []

# We'll use this flag to tell our SSE listener thread to stop when the app shuts down.
if "stop_sse" not in st.session_state:
    st.session_state["stop_sse"] = False


def sse_listener():
    """
    Background thread that connects (and reconnects) to the SSE endpoint,
    listens for new events, and stores them in session state.

    Because `sseclient` does NOT automatically reconnect, we manually
    wrap the connection logic in a loop. This way, if it disconnects
    due to network issues, it tries again until `stop_sse` is True.
    """
    while not st.session_state["stop_sse"]:
        # Optional: build headers if you need authentication
        headers = {}
        if "token" in st.session_state:
            headers["Authorization"] = f"Bearer {st.session_state['token']}"

        try:
            # Attempt to open a streaming connection to the SSE endpoint
            with requests.get(f"{API_URL}/sse", headers=headers, stream=True) as response:
                # Initialize sseclient with the open response
                client = SSEClient(response)
                
                # Iterate over each incoming SSE event
                for event in client.events():
                    # If the main thread signaled we should stop, break
                    if st.session_state["stop_sse"]:
                        break

                    # Parse the data from SSE (event.data is a string)
                    try:
                        data = json.loads(event.data)
                        # Append the incoming message to our notifications in session state
                        st.session_state["notifications"].append(data)
                        
                        # Force Streamlit to re-run, so the UI updates with the new message
                        st.experimental_rerun()
                    except json.JSONDecodeError as e:
                        print("Failed to parse SSE data:", e)
                    except Exception as e:
                        print("General exception while handling SSE event:", e)

        except Exception as e:
            # If anything goes wrong (server down, network issue, etc.),
            # we print the error and try again after a short delay.
            print("Error connecting to SSE endpoint:", e)

        # Small delay before retrying to avoid rapid loops if server is unreachable
        time.sleep(2)


def start_sse_thread():
    """
    Start the SSE listener thread (if it's not already running).
    """
    # Only start if there's no thread or if the existing thread is not alive
    if "sse_thread" not in st.session_state or not st.session_state["sse_thread"].is_alive():
        st.session_state["stop_sse"] = False
        
        # Create and start the background thread
        thread = threading.Thread(target=sse_listener, daemon=True)
        thread.start()
        
        # Store the thread object in session state so we can manage it later
        st.session_state["sse_thread"] = thread


def stop_sse_thread():
    """
    Signal the SSE listener to stop.
    """
    # Set the flag that tells the listener loop to break
    st.session_state["stop_sse"] = True
    
    # If we have a running thread, join it briefly to allow cleanup
    if "sse_thread" in st.session_state and st.session_state["sse_thread"].is_alive():
        st.session_state["sse_thread"].join(timeout=1)


def show_tasks():
    """
    Displays the task management interface, including creating, viewing, and deleting tasks.
    """
    # Ensure the user is logged in (this is just an example check)
    if "token" not in st.session_state:
        st.warning("Please log in to access tasks.")
        return

    st.title("Task Management")

    # 1. Start SSE in the background (so we can get real-time notifications)
    start_sse_thread()

    # 2. Task creation form
    st.header("Create a New Task")
    title = st.text_input("Task Title")
    description = st.text_area("Task Description")

    # (Optional) Retrieve the logged-in user's ID from session state
    assigned_user_id = st.session_state.get("user_id", None)

    if st.button("Create Task"):
        task_data = {
            "title": title,
            "description": description,
            "assigned_user_id": assigned_user_id
        }
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        response = requests.post(f"{API_URL}/tasks/", json=task_data, headers=headers)
        
        if response.status_code == 200:
            st.success("Task created successfully!")
        else:
            st.error("Error creating task.")

    # 3. List tasks
    st.header("Your Tasks")
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(
        f"{API_URL}/tasks/?assigned_user_id={assigned_user_id}", headers=headers
    )
    tasks = response.json()

    for task in tasks:
        st.subheader(task["title"])
        st.write(task["description"])
        st.write("Status:", task["status"])
        
        if st.button(f"Delete {task['title']}", key=task["task_id"]):
            delete_response = requests.delete(
                f"{API_URL}/tasks/{task['task_id']}", headers=headers
            )
            if delete_response.status_code == 200:
                st.success("Task deleted successfully")
                st.experimental_rerun()
            else:
                st.error("Error deleting task")

    # 4. Display Real-Time Notifications
    st.header("Real-Time Notifications")
    # Show each notification as a small collapsible section
    for idx, note in enumerate(st.session_state["notifications"]):
        with st.expander(f"Notification #{idx + 1}", expanded=False):
            st.write(note)


# Cleanup logic: ensure we stop the SSE thread when the script stops or re-runs
def cleanup_sse_thread():
    stop_sse_thread()

# When the Streamlit session ends, call our cleanup
st.on_session_end(cleanup_sse_thread)
