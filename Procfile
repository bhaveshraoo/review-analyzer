web: python3 -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT
worker: python3 -m celery -A backend.tasks.celery_app.celery_app worker --loglevel=info --pool=threads