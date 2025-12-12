from fastapi import APIRouter, Depends, HTTPException
import uuid6
from sqlalchemy.orm import Session

from .auth import verify_api_key
from backend.database import SessionLocal
from backend.master_agent.models.job import Job
from backend.common.schemas.api_requests import ResearchRequest


router = APIRouter()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.post("/api/research", dependencies=[Depends(verify_api_key)])
async def create_research_job(
    request: ResearchRequest,
    db: Session = Depends(get_db)
):
    job = Job(
        id=uuid6.uuid7(),
        prompt=request.prompt,
        status="queued"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return {"job_id": str(job.id)}

@router.get("/api/research/{job_id}/status", dependencies=[Depends(verify_api_key)])
async def get_research_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(404, "Job not found")
    return {
        "job_id": str(job.id),
        "status": job.status,
        "canonical_result": job.canonical_result,
        "created_at": job.created_at
    }