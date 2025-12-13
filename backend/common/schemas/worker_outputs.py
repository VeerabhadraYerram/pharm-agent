from pydantic import BaseModel
from typing import List
from .canonical_result import TrialRecord


class ClinicalTrialsOutputs(BaseModel):
    trials: List[TrialRecord]
    summary_text: str
    research_confidence: float
    key_findings: List[str]
    suggested_follow_up: List[str]