from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from .auth import verify_worker_token
from backend.database import SessionLocal
from backend.common.schemas.worker_envelope import WorkerEnvelope
from backend.master_agent.models.worker_response import WorkerResponse


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/internal/task/{task_id}/complete",
    dependencies=[Depends(verify_worker_token)]
)
async def worker_callback(task_id: str, request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    envelope = WorkerEnvelope(**body)

    # convert typed models to JSON-safe dicts
    sources_json = [s.model_dump(mode="json") for s in envelope.sources]

    db_row = WorkerResponse(
        task_id=envelope.task_id,
        job_id=envelope.job_id,
        worker=envelope.worker,
        status=envelope.status,
        confidence=envelope.confidence,
        timestamp=envelope.timestamp,
        outputs=envelope.outputs,
        sources=sources_json,
        notes=envelope.notes,
        raw_envelope=body,
    )

    db.add(db_row)
    db.commit()
    db.refresh(db_row)

    return {"status": "stored", "task_id": str(envelope.task_id)}

