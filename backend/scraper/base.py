from abc import ABC, abstractmethod
from typing import List, Dict

class BaseScraper(ABC):
    def __init__(self, url: str, max_reviews: int = 100):
        self.url = url
        self.max_reviews = max_reviews

    @abstractmethod
    def scrape(self) -> List[Dict]:
        """Returns list of dicts with keys: text, rating, date"""
        pass