# frontend/main.py
import streamlit as st
import requests

API_URL = "http://localhost:8000/auth"

def register_user(username, email, password):
    response = requests.post(f"{API_URL}/register", json={"username": username, "email": email, "password": password})
    return response.json()

def login_user(username, password):
    response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    return response.json()

st.title("Task Manager - Authentication")

choice = st.selectbox("Select Action", ["Login", "Register"])

if choice == "Register":
    st.subheader("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        response = register_user(username, email, password)
        st.write(response)

if choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = login_user(username, password)
        if "access_token" in response:
            st.session_state["token"] = response["access_token"]
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")
