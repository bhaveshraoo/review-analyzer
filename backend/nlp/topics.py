from keybert import KeyBERT
from typing import List, Dict

kw_model = KeyBERT()

def extract_topics(reviews: List[str], top_n: int = 6) -> List[Dict]:
    combined = " ".join(reviews)
    try:
        keywords = kw_model.extract_keywords(
            combined,
            keyphrase_ngram_range=(1, 2),
            stop_words="english",
            top_n=top_n
        )
        return [{"keyword": kw, "score": round(score, 3)} for kw, score in keywords]
    except Exception as e:
        print(f"Topic extraction error: {e}")
        return []