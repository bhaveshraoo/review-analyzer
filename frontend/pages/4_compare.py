import streamlit as st
import requests
import plotly.graph_objects as go
import os

<<<<<<< HEAD
API_BASE = "https://web-production-4e424.up.railway.app"
=======
API_BASE = os.environ.get("BACKEND_URL", "http://localhost:8000")
>>>>>>> 49b3ecf (Auto create tables on startup)

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please login first")
    st.stop()

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

with st.sidebar:
    st.markdown("## 📊 Review Analyzer")
    st.divider()
    st.page_link("pages/1_dashboard.py",  label="📊 Dashboard")
    st.page_link("pages/2_submit_job.py", label="🔍 Analyze Reviews")
    st.page_link("pages/3_reports.py",    label="📁 Past Reports")
    st.page_link("pages/4_compare.py",    label="⚖️ Compare Products")
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.token = None
        st.rerun()

st.title("⚖️ Compare Products")
st.markdown("Select two analyses to compare side by side")
st.divider()

jobs_res = requests.get(f"{API_BASE}/reviews/list", headers=get_headers())
jobs = jobs_res.json() if jobs_res.status_code == 200 else []
done_jobs = [j for j in jobs if j["status"] == "done"]

if len(done_jobs) < 2:
    st.warning("You need at least 2 completed analyses to compare. Submit more jobs first.")
    st.stop()

job_options = {f"{j['url'][8:50]}...": j["id"] for j in done_jobs}

col1, col2 = st.columns(2)
with col1:
    job1_label = st.selectbox("Product A", list(job_options.keys()), key="job1")
with col2:
    job2_label = st.selectbox("Product B", list(job_options.keys()), key="job2",
                              index=min(1, len(job_options)-1))

if job1_label == job2_label:
    st.warning("Please select two different analyses.")
    st.stop()

res1 = requests.get(f"{API_BASE}/reviews/{job_options[job1_label]}", headers=get_headers()).json()
res2 = requests.get(f"{API_BASE}/reviews/{job_options[job2_label]}", headers=get_headers()).json()

r1 = res1.get("result", {})
r2 = res2.get("result", {})
s1 = r1.get("sentiment", {})
s2 = r2.get("sentiment", {})

st.divider()
st.markdown("### 📊 Side by Side Metrics")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**{job1_label}**")
    st.metric("Total Reviews", r1.get("total_reviews", 0))
    st.metric("Positive", f"{s1.get('positive', 0)}%")
    st.metric("Negative", f"{s1.get('negative', 0)}%")
    st.metric("Avg Rating", r1.get("avg_rating", "N/A"))

with col2:
    st.markdown(f"**{job2_label}**")
    st.metric("Total Reviews", r2.get("total_reviews", 0),
              delta=str(r2.get("total_reviews", 0) - r1.get("total_reviews", 0)))
    st.metric("Positive", f"{s2.get('positive', 0)}%",
              delta=f"{s2.get('positive', 0) - s1.get('positive', 0)}%")
    st.metric("Negative", f"{s2.get('negative', 0)}%",
              delta=f"{s2.get('negative', 0) - s1.get('negative', 0)}%",
              delta_color="inverse")
    st.metric("Avg Rating", r2.get("avg_rating", "N/A"))

st.divider()
st.markdown("### 📈 Sentiment Comparison")

categories = ["Positive", "Negative", "Neutral"]
fig = go.Figure()
fig.add_trace(go.Bar(
    name=job1_label[:30],
    x=categories,
    y=[s1.get("positive", 0), s1.get("negative", 0), s1.get("neutral", 0)],
    marker_color="#1D9E75"
))
fig.add_trace(go.Bar(
    name=job2_label[:30],
    x=categories,
    y=[s2.get("positive", 0), s2.get("negative", 0), s2.get("neutral", 0)],
    marker_color="#534AB7"
))
fig.update_layout(
    barmode="group",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#FAFAFA",
    margin=dict(t=10, b=10)
)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("### 🤖 AI Summaries")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**{job1_label}**")
    st.info(r1.get("summary", "No summary"))
with col2:
    st.markdown(f"**{job2_label}**")
    st.info(r2.get("summary", "No summary"))