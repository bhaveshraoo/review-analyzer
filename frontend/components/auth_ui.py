import streamlit as st
import requests

API_BASE = "http://localhost:8000"

def show_login():
    st.title("📊 Review Analyzer")
    st.markdown("AI-powered product review analysis")
    st.divider()

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", use_container_width=True):
            res = requests.post(f"{API_BASE}/auth/login",
                                json={"email": email, "password": password})
            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register", use_container_width=True):
            res = requests.post(f"{API_BASE}/auth/register",
                                json={"email": email, "password": password})
            if res.status_code == 201:
                st.success("Account created — please log in")
            else:
                st.error("Registration failed")