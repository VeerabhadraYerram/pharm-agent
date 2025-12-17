import uuid6
from sqlalchemy.orm import Session
from backend.master_agent.models.job import Job


class JobService:
    # handle db operations for job lifecycle.

    @staticmethod
    def create_job(db: Session, prompt_original: str, prompt_normalized: str, molecule: str) -> Job:
        job = Job(
            id = uuid6.uuid7(),
            user_id = None,
            prompt_original = prompt_original,
            prompt_normalized = prompt_normalized,
            molecule = molecule,
            status = "running"
        )

        db.add(job)
        db.commit()
        db.refresh(job)
        return job
    
    @staticmethod
    def update_canonical_result(db: Session, job_id, canonical_json: dict) -> Job:
        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            raise ValueError(f"Job {job_id} not found")
        
        job.canonical_result = canonical_json
        job.status = "completed"

        db.add(job)
        db.commit()
        db.refresh(job)

        return job