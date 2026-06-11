import streamlit as st
import requests
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

API_BASE = "https://web-production-4e424.up.railway.app"

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please login first")
    st.stop()

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

# ── Sidebar ──────────────────────────────────────────────────
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

st.title("📊 Dashboard")

# ── Load jobs ────────────────────────────────────────────────
jobs_res = requests.get(f"{API_BASE}/reviews/list", headers=get_headers())
jobs = jobs_res.json() if jobs_res.status_code == 200 else []
done_jobs = [j for j in jobs if j["status"] == "done" and j.get("result")]

if not done_jobs:
    st.info("No completed analyses yet. Go to **Analyze Reviews** to get started.")
    st.stop()
def get_app_name(url):
    if "id=" in url:
        pkg = url.split("id=")[-1].split("&")[0]
        name = pkg.split(".")[-1].replace("-", " ").title()
        return name
    return url[8:40]

job_options = {f"{get_app_name(j['url'])} ({j['created_at'][:10]})": j["id"] for j in done_jobs}
selected_label = st.selectbox("Select analysis", list(job_options.keys()))
job_id = job_options[selected_label]

res = requests.get(f"{API_BASE}/reviews/{job_id}", headers=get_headers())
data = res.json() if res.status_code == 200 else {}
result = data.get("result", {})

if not result or result.get("total_reviews", 0) == 0:
    st.warning("This job has no review data. Please select another job or submit a new one.")
    st.stop()

sentiment = result.get("sentiment", {})
topics    = result.get("topics", [])
raw_texts = result.get("raw_texts", [])
per_review = sentiment.get("per_review", [])

# ── Metric cards ─────────────────────────────────────────────
st.markdown("### Overview")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("📝 Total Reviews", result.get("total_reviews", 0))
col2.metric("😊 Positive", f"{sentiment.get('positive', 0)}%",
            delta=f"+{sentiment.get('positive', 0) - 50}% vs avg" if sentiment.get('positive', 0) > 50 else None)
col3.metric("😠 Negative", f"{sentiment.get('negative', 0)}%",
            delta=f"{sentiment.get('negative', 0) - 20}% vs avg",
            delta_color="inverse")
col4.metric("😐 Neutral", f"{sentiment.get('neutral', 0)}%")
col5.metric("⭐ Avg Rating", result.get("avg_rating", "N/A"))

st.divider()

# ── Charts row ───────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📊 Sentiment Breakdown")
    fig = go.Figure(go.Bar(
        x=["Positive", "Negative", "Neutral"],
        y=[sentiment.get("positive", 0),
           sentiment.get("negative", 0),
           sentiment.get("neutral",  0)],
        marker_color=["#1D9E75", "#D85A30", "#888780"],
        text=[f"{sentiment.get('positive', 0)}%",
              f"{sentiment.get('negative', 0)}%",
              f"{sentiment.get('neutral',  0)}%"],
        textposition="auto"
    ))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FAFAFA",
        margin=dict(t=10, b=10),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown("### 🍩 Sentiment Distribution")
    fig2 = go.Figure(go.Pie(
        labels=["Positive", "Negative", "Neutral"],
        values=[sentiment.get("positive", 0),
                sentiment.get("negative", 0),
                sentiment.get("neutral",  0)],
        hole=0.5,
        marker_colors=["#1D9E75", "#D85A30", "#888780"]
    ))
    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FAFAFA",
        margin=dict(t=10, b=10)
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── AI Summary ───────────────────────────────────────────────
st.markdown("### 🤖 AI Summary")
summary = result.get("summary", "No summary available")
if "429" in summary or "quota" in summary.lower():
    summary = "AI summary temporarily unavailable. Sentiment and topic analysis above are fully accurate."
st.info(summary)
if sentiment.get("negative", 0) > 30:
    st.error(f"⚠️ High negative sentiment ({sentiment.get('negative')}%) — action recommended!")
elif sentiment.get("positive", 0) > 70:
    st.success(f"🎉 Excellent sentiment! {sentiment.get('positive')}% positive reviews.")

st.divider()

# ── Topics ───────────────────────────────────────────────────
st.markdown("### 🏷️ Top Topics")
if topics:
    topic_cols = st.columns(len(topics))
    for i, topic in enumerate(topics):
        score_pct = int(topic['score'] * 100)
        topic_cols[i].markdown(
            f"""<div style='background:#1A2E25;border:1px solid #1D9E75;
            border-radius:12px;padding:12px;text-align:center'>
            <div style='color:#1D9E75;font-size:13px;font-weight:600'>{topic['keyword']}</div>
            <div style='color:#888;font-size:11px;margin-top:4px'>{score_pct}% relevance</div>
            </div>""",
            unsafe_allow_html=True
        )

st.divider()

# ── Sentiment trend ──────────────────────────────────────────
st.markdown("### 📈 Sentiment Trend (per review)")
if per_review:
    sentiment_map = {"positive": 1, "neutral": 0, "negative": -1}
    y_vals = [sentiment_map.get(r["sentiment"], 0) for r in per_review]
    x_vals = list(range(1, len(y_vals) + 1))
    colors = ["#1D9E75" if v == 1 else "#D85A30" if v == -1 else "#888780" for v in y_vals]

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=x_vals, y=y_vals,
        mode="lines+markers",
        line=dict(color="#1D9E75", width=2),
        marker=dict(color=colors, size=8),
        hovertext=[r["text"][:80] for r in per_review],
        hoverinfo="text"
    ))
    fig3.add_hline(y=0, line_dash="dash", line_color="#888780", opacity=0.5)
    fig3.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FAFAFA",
        yaxis=dict(tickvals=[-1, 0, 1],
                   ticktext=["Negative", "Neutral", "Positive"]),
        xaxis_title="Review #",
        margin=dict(t=10, b=10)
    )
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ── Review search & filter ───────────────────────────────────
st.markdown("### 🔎 Search & Filter Reviews")
col_search, col_filter = st.columns([2, 1])
with col_search:
    search_query = st.text_input("Search reviews", placeholder="e.g. delivery, crash, update")
with col_filter:
    filter_sentiment = st.selectbox("Filter by sentiment", ["All", "Positive", "Negative", "Neutral"])

filtered = per_review
if search_query:
    filtered = [r for r in filtered if search_query.lower() in r["text"].lower()]
if filter_sentiment != "All":
    filtered = [r for r in filtered if r["sentiment"] == filter_sentiment.lower()]

st.markdown(f"Showing **{len(filtered)}** reviews")
for r in filtered[:20]:
    color = "#1D9E75" if r["sentiment"] == "positive" else "#D85A30" if r["sentiment"] == "negative" else "#888780"
    icon  = "😊" if r["sentiment"] == "positive" else "😠" if r["sentiment"] == "negative" else "😐"
    st.markdown(
        f"""<div style='border-left:3px solid {color};padding:8px 12px;
        margin:6px 0;background:#1A1D23;border-radius:0 8px 8px 0'>
        <span style='color:{color}'>{icon} {r['sentiment'].upper()}</span>
        <p style='margin:4px 0;color:#FAFAFA;font-size:13px'>{r['text']}</p>
        </div>""",
        unsafe_allow_html=True
    )

st.divider()

# ── Word cloud ───────────────────────────────────────────────
st.markdown("### ☁️ Word Cloud")
if raw_texts:
    all_text = " ".join(raw_texts)
    wc = WordCloud(
        width=1000, height=350,
        background_color="#0E1117",
        colormap="Greens",
        max_words=100
    ).generate(all_text)
    fig_wc, ax = plt.subplots(figsize=(12, 4))
    fig_wc.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig_wc)