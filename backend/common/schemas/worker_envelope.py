from pydantic import BaseModel
from typing import Any, List
from datetime import datetime
import uuid


class WorkerSource(BaseModel):
    type: str
    title: str | None = None
    uri: str | None = None
    retrieved_at: datetime | None = None

class WorkerEnvelope(BaseModel):
    job_id: uuid.UUID
    task_id: uuid.UUID
    worker: str
    status: str
    confidence: float
    timestamp: datetime
    outputs: Any    # worker specific
    sources: List[WorkerSource]
    notes: str | None = None