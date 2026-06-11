from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.auth.utils import get_current_user
from backend.auth.models import User
from backend.reviews.models import ReviewJob
from backend.reviews.schemas import SubmitJobRequest, JobOut

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/submit", response_model=JobOut, status_code=202)
def submit_job(
    payload: SubmitJobRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = ReviewJob(
        user_id=current_user.id,
        url=payload.url,
        source=payload.source,
        max_reviews=payload.max_reviews,
        status="pending"
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    from backend.tasks.analyze_task import run_analysis
    run_analysis.delay(str(job.id))

    return job

@router.get("/list", response_model=List[JobOut])
def list_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(ReviewJob).filter(
        ReviewJob.user_id == current_user.id
    ).order_by(ReviewJob.created_at.desc()).all()

@router.get("/{job_id}", response_model=JobOut)
def get_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = db.query(ReviewJob).filter(
        ReviewJob.id == job_id,
        ReviewJob.user_id == current_user.id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job