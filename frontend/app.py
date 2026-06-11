import streamlit as st

st.set_page_config(
    page_title="Review Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token is None:
    from components.auth_ui import show_login
    show_login()
else:
    st.switch_page("pages/1_dashboard.py")