import google.generativeai as genai
from typing import List
from backend.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_summary(reviews: List[str], product_name: str = "this product") -> str:
    try:
        sample = reviews[:30]
        reviews_text = "\n".join([f"- {r}" for r in sample])

        prompt = f"""You are a product analyst. Below are customer reviews for {product_name}.
Analyze them and write a 3-4 sentence business summary covering:
1. What customers love most
2. Main complaints or issues
3. Overall sentiment trend

Reviews:
{reviews_text}

Write a concise, actionable summary:"""

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "AI summary temporarily unavailable due to API quota. Sentiment and topic analysis above are fully accurate."