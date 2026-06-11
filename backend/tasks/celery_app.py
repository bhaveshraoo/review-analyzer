from celery import Celery
from backend.config import settings

celery_app = Celery(
    "review_analyzer",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["backend.tasks.analyze_task"]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    worker_pool="threads",  # use threads instead of fork
)