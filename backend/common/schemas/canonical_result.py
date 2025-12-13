from pydantic import BaseModel, Field
from typing import Any, List, Optional, Dict


class TrialRecord(BaseModel):
    nct_id: str
    phase: str
    status: str
    condition: str
    region: Optional[str] = None
    results_summary: Optional[str] = None

class CanonicalResult(BaseModel):
    molecule: str
    trial_summary: Optional[str] = None
    trials: List[TrialRecord] = Field(default_factory=list)
    key_findings: List[str] = Field(default_factory=list)
    suggested_follow_up: List[str] = Field(default_factory=list)
    data_completeness_score: Optional[float] = None
    confidence_overall: Optional[float] = None
    synthesis_version: str = "0.1.0"