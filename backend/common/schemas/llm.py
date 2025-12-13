from pydantic import BaseModel
from typing import List

class ClinicalLLMResponse(BaseModel):
    summary_text: str
    research_confidence: float
    key_findings: List[str]
    suggested_follow_up: List[str]