import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
from backend.scraper.base import BaseScraper

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
}

class AmazonScraper(BaseScraper):
    def scrape(self) -> List[Dict]:
        reviews = []
        try:
            response = httpx.get(self.url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            review_divs = soup.select("div[data-hook='review']")

            for div in review_divs[:self.max_reviews]:
                text_el   = div.select_one("span[data-hook='review-body']")
                rating_el = div.select_one("i[data-hook='review-star-rating']")
                date_el   = div.select_one("span[data-hook='review-date']")

                if text_el:
                    reviews.append({
                        "text":   text_el.get_text(strip=True),
                        "rating": rating_el.get_text(strip=True) if rating_el else "N/A",
                        "date":   date_el.get_text(strip=True) if date_el else "N/A",
                    })
        except Exception as e:
            print(f"Amazon scrape error: {e}")
        return reviews