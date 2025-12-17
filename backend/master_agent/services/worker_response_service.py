import uuid
from sqlalchemy.orm import Session

from backend.master_agent.services.task_service import TaskService
from backend.master_agent.models.worker_response import WorkerResponse
from backend.common.schemas.worker_envelope import WorkerEnvelope


class WorkerResponseService:
    # stores worker envelopes and updates task status

    @staticmethod
    def save_worker_response(db: Session, envelope: WorkerEnvelope) -> WorkerResponse:
        # persist worker envelope into db and mark task completed.

        # 1. create orm object
        response = WorkerResponse(
            id = envelope.id or envelope.task_id,
            task_id = envelope.task_id,
            job_id = envelope.job_id,
            worker = envelope.worker,
            status = envelope.status,
            confidence = envelope.confidence,
            timestamp = envelope.timestamp,
            outputs = envelope.outputs,
            sources = [src.model_dump(model="json") for src in envelope.sources],
            notes = envelope.notes
        )

        db.add(response)
        db.commit()
        db.refresh(response)

        # 2. update task row
        if envelope.status == "ok":
            TaskService.mark_completed(db, envelope.task_id)
        else:
            TaskService.mark_failed(db, envelope.task_id, envelope.notes or "Worker error")

        return response
    
    @staticmethod
    def get_response_for_task(db: Session, task_id: uuid.UUID) -> WorkerResponse | None:
        return (
            db.query(WorkerResponse)
                .filter(WorkerResponse.task_id == task_id)
                .first()
        )