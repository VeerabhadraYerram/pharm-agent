from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from .canonical_result import TrialRecord


class ClinicalTrialsOutputs(BaseModel):
    trials: List[TrialRecord]
    summary_text: str
    research_confidence: float
    key_findings: List[str]
    suggested_follow_up: List[str]

class ReportWorkerOutputs(BaseModel):
    pdf_uri: str
    ppt_uri: str

class MarketIntelligenceOutputs(BaseModel):
    market_size: Optional[str] = None
    competitors: List[Dict[str, Any]] = []
    patent_status: Optional[str] = None
    pricing_insights: Optional[str] = None
    key_findings: List[str] = []