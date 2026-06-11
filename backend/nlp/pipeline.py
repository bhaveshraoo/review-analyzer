from typing import List, Dict
from backend.nlp.sentiment import analyze_sentiment
from backend.nlp.topics import extract_topics
from backend.nlp.summarizer import generate_summary

def run_nlp_pipeline(reviews: List[Dict]) -> Dict:
    texts = [r["text"] for r in reviews if r.get("text")]
    ratings = [r["rating"] for r in reviews if isinstance(r.get("rating"), (int, float))]

    if not texts:
        return {"error": "No review texts found"}

    sentiment = analyze_sentiment(texts)
    topics    = extract_topics(texts)
    summary   = generate_summary(texts)

    avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else None

    return {
        "total_reviews": len(texts),
        "avg_rating":    avg_rating,
        "sentiment":     sentiment,
        "topics":        topics,
        "summary":       summary,
        "raw_texts":     texts[:50]
    }