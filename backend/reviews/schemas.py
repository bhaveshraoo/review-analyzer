from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class SubmitJobRequest(BaseModel):
    url: str
    source: str  # "amazon" or "google_play"
    max_reviews: int = 100

class JobOut(BaseModel):
    id: UUID
    url: str
    source: str
    status: str
    result: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True