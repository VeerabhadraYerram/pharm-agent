import pytest
from unittest.mock import MagicMock, patch
from backend.workers.patent_worker.worker import run_patent_worker
from backend.common.schemas.canonical_result import PatentOutputs, PatentRecord

def test_run_patent_worker_success():
    # Mock parameters
    job_id = "00000000-0000-0000-0000-000000000000"
    task_id = "00000000-0000-0000-0000-000000000001"
    params = {"molecule": "Aspirin"}

    # Mock LLM response
    mock_outputs = PatentOutputs(patents=[
        PatentRecord(
            patent_id="US1234567",
            title="Method of synthesis for Aspirin",
            status="Expired",
            summary="A novel method for synthesizing acetylsalicylic acid."
        )
    ])

    # Patch the llm_structured call
    with patch("backend.workers.patent_worker.worker.llm_structured") as mock_llm:
        mock_llm.return_value = mock_outputs
        
        # Run worker
        result = run_patent_worker(job_id, task_id, params)
        
        # Verify
        assert result["worker"] == "patent_worker"
        assert result["status"] == "ok"
        assert len(result["outputs"]["patents"]) == 1
        assert result["outputs"]["patents"][0]["patent_id"] == "US1234567"
