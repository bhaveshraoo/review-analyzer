from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from backend.database import Base

class ReviewJob(Base):
    __tablename__ = "review_jobs"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id     = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    url         = Column(String, nullable=False)
    source      = Column(String, nullable=False)
    max_reviews = Column(Integer, default=100)
    status      = Column(String, default="pending")  # pending/running/done/failed
    result      = Column(JSON, nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())