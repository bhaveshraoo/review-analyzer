from fastapi import FastAPI
from backend.auth.routes import router as auth_router
from backend.reviews.routes import router as reviews_router
from backend.database import engine, Base
from backend.auth.models import User
from backend.reviews.models import ReviewJob

# Auto-create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Review Analyzer API")
app.include_router(auth_router)
app.include_router(reviews_router)
