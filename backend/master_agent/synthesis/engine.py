from uuid import UUID
from sqlalchemy.orm import Session


def run_synthesis(job_id: UUID, db: Session) -> dict:
    # stub
    """
    - collect all WorkerResponse rows for job
    - perform domain reasoning
    - produce canonical_result
    """
    return {}