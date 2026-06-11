import plotly.express as px
import plotly.graph_objects as go

def sentiment_bar_chart(sentiment: dict):
    labels = ["Positive", "Negative", "Neutral"]
    values = [
        sentiment.get("positive", 0),
        sentiment.get("negative", 0),
        sentiment.get("neutral", 0)
    ]
    colors = ["#1D9E75", "#D85A30", "#888780"]
    fig = px.bar(
        x=labels, y=values,
        color=labels,
        color_discrete_sequence=colors,
        labels={"x": "", "y": "% of reviews"}
    )
    fig.update_layout(showlegend=False, margin=dict(t=10, b=10))
    return fig

def rating_gauge(avg_rating: float):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_rating,
        domain={"x": [0, 1], "y": [0, 1]},
        gauge={
            "axis": {"range": [0, 5]},
            "bar": {"color": "#1D9E75"},
            "steps": [
                {"range": [0, 2], "color": "#FAECE7"},
                {"range": [2, 3.5], "color": "#FAEEDA"},
                {"range": [3.5, 5], "color": "#E1F5EE"},
            ]
        }
    ))
    fig.update_layout(height=200, margin=dict(t=10, b=10))
    return fig