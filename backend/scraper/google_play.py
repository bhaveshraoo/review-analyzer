from google_play_scraper import reviews, Sort
from typing import List, Dict
from backend.scraper.base import BaseScraper

class GooglePlayScraper(BaseScraper):
    def _extract_app_id(self) -> str:
        if "id=" in self.url:
            return self.url.split("id=")[-1].split("&")[0]
        return self.url

    def scrape(self) -> List[Dict]:
        result = []
        try:
            app_id = self._extract_app_id()
            raw, _ = reviews(
                app_id,
                lang="en",
                country="us",
                sort=Sort.NEWEST,
                count=self.max_reviews
            )
            for r in raw:
                result.append({
                    "text":   r["content"],
                    "rating": r["score"],
                    "date":   str(r["at"]),
                })
        except Exception as e:
            print(f"Google Play scrape error: {e}")
        return result