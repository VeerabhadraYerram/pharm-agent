from pydantic import BaseModel
import uuid


class ResearchRequest(BaseModel):
    prompt: str

class ResearchStatusResponse(BaseModel):
    job_id: uuid.UUID
    status: str
    canonical_result: dict | None = None