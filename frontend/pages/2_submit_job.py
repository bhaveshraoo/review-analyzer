import streamlit as st
import requests

API_BASE = "http://localhost:8000"

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please login first")
    st.stop()

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

st.title("🔍 Analyze Reviews")
st.markdown("Submit a product URL to start analysis")
st.divider()

with st.form("submit_form"):
    url = st.text_input("Product / App URL",
                        placeholder="https://play.google.com/store/apps/details?id=com.whatsapp")
    source = st.selectbox("Source", ["Google Play", "Amazon"])
    max_reviews = st.slider("Max reviews to fetch", 10, 200, 50, step=10)
    submitted = st.form_submit_button("Start Analysis", use_container_width=True)

if submitted and url:
    with st.spinner("Submitting job..."):
        res = requests.post(
            f"{API_BASE}/reviews/submit",
            json={"url": url, "source": source.lower().replace(" ", "_"), "max_reviews": max_reviews},
            headers=get_headers()
        )
        if res.status_code == 202:
            job = res.json()
            st.success(f"Job queued! ID: `{job['id']}`")
            st.session_state["last_job_id"] = job["id"]
            st.info("Go to Dashboard to see results once analysis completes (~30 seconds)")
        else:
            st.error("Submission failed. Please try again.")