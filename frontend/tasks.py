import streamlit as st
import requests

API_URL = "http://localhost:8000"

def show_tasks():
    """
    Displays the task management interface, including creating, viewing, and deleting tasks.
    """
    # Ensure the user is logged in
    if "token" not in st.session_state:
        st.warning("Please log in to access tasks.")
        return

    # Display task creation form
    st.header("Create a New Task")
    title = st.text_input("Task Title")
    description = st.text_area("Task Description")
    assigned_user_id = st.session_state['user_id']  # Get logged-in user's ID

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

    # Display list of tasks
    st.header("Your Tasks")
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{API_URL}/tasks/?assigned_user_id={assigned_user_id}", headers=headers)
    tasks = response.json()

    for task in tasks:
        st.subheader(task['title'])
        st.write(task['description'])
        st.write("Status:", task['status'])
        if st.button(f"Delete {task['title']}", key=task['task_id']):
            delete_response = requests.delete(f"{API_URL}/tasks/{task['task_id']}", headers=headers)
            if delete_response.status_code == 200:
                st.success("Task deleted successfully")
                st.experimental_rerun()  # Refresh the task list
            else:
                st.error("Error deleting task")
