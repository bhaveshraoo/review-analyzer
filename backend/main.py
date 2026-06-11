from fastapi import FastAPI
from backend.auth.routes import router as auth_router
from backend.reviews.routes import router as reviews_router

app = FastAPI(title="Review Analyzer API")
app.include_router(auth_router)
app.include_router(reviews_router)