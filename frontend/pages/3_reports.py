import streamlit as st
import requests

API_BASE = "https://web-production-4e424.up.railway.app"

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please login first")
    st.stop()

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

st.title("📁 Past Reports")
st.divider()

jobs_res = requests.get(f"{API_BASE}/reviews/list", headers=get_headers())
jobs = jobs_res.json() if jobs_res.status_code == 200 else []

if not jobs:
    st.info("No past reports found.")
    st.stop()

for job in jobs:
    status_icon = {"done": "✅", "running": "⏳", "pending": "🕐", "failed": "❌"}.get(job["status"], "❓")
    with st.expander(f"{status_icon} {job['url'][:60]} — {job['created_at'][:10]}"):
        st.write(f"**Job ID:** `{job['id']}`")
        st.write(f"**Source:** {job['source']}")
        st.write(f"**Status:** {job['status'].upper()}")
        if job["status"] == "done" and job.get("result"):
            result = job["result"]
            col1, col2, col3 = st.columns(3)
            col1.metric("Reviews", result.get("total_reviews", 0))
            col2.metric("Positive", f"{result.get('sentiment', {}).get('positive', 0)}%")
            col3.metric("Avg Rating", result.get("avg_rating", "N/A"))