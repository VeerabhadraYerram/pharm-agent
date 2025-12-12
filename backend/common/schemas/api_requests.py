from pydantic import BaseModel
import uuid


class ResearchRequest(BaseModel):
    prompt: str
    molecule: str
    indications: list[str] = []

class ResearchStatusResponse(BaseModel):
    job_id: uuid.UUID
    status: str