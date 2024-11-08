import streamlit as st
from auth import show_authentication
from tasks import show_tasks

# Check if user is logged in
if "token" not in st.session_state:
    # If not logged in, show authentication page
    show_authentication()
else:
    # If logged in, show task management page
    show_tasks()
