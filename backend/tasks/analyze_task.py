from backend.tasks.celery_app import celery_app
from backend.database import SessionLocal
from backend.auth.models import User
from backend.reviews.models import ReviewJob

@celery_app.task
def run_analysis(job_id: str):
    db = SessionLocal()
    try:
        job = db.query(ReviewJob).filter(ReviewJob.id == job_id).first()
        if not job:
            return

        job.status = "running"
        db.commit()

        if job.source == "amazon":
            from backend.scraper.amazon import AmazonScraper
            scraper = AmazonScraper(job.url, job.max_reviews)
        else:
            from backend.scraper.google_play import GooglePlayScraper
            scraper = GooglePlayScraper(job.url, job.max_reviews)

        reviews = scraper.scrape()

        from backend.nlp.pipeline import run_nlp_pipeline
        nlp_result = run_nlp_pipeline(reviews)

        job.result = nlp_result
        job.status = "done"
        db.commit()

    except Exception as e:
        db.rollback()
        job.status = "failed"
        job.result = {"error": str(e)}
        db.commit()
    finally:
        db.close()