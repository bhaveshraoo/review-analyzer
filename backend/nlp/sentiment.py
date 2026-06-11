from transformers import pipeline
from typing import List, Dict

sentiment_model = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    truncation=True,
    max_length=512
)

LABEL_MAP = {
    "positive": "positive",
    "negative": "negative",
    "neutral":  "neutral",
    "LABEL_0":  "negative",
    "LABEL_1":  "neutral",
    "LABEL_2":  "positive",
}

def analyze_sentiment(reviews: List[str]) -> Dict:
    counts = {"positive": 0, "negative": 0, "neutral": 0}
    per_review = []

    for text in reviews:
        try:
            result = sentiment_model(text[:512])[0]
            label = LABEL_MAP.get(result["label"], "neutral")
            counts[label] += 1
            per_review.append({"text": text, "sentiment": label})
        except Exception:
            counts["neutral"] += 1
            per_review.append({"text": text, "sentiment": "neutral"})

    total = len(reviews) or 1
    return {
        "positive": round(counts["positive"] / total * 100),
        "negative": round(counts["negative"] / total * 100),
        "neutral":  round(counts["neutral"]  / total * 100),
        "per_review": per_review
    }
