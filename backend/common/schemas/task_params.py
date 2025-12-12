import uuid
from pydantic import BaseModel
from typing import Any


class TaskParams(BaseModel):
    job_id: uuid.UUID
    task_id: uuid.UUID
    worker_type: str
    params: dict[str, Any]