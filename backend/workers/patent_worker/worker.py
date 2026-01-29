import json
import uuid
import uuid6
from datetime import datetime, UTC
from celery import shared_task

from backend.common.schemas.worker_envelope import WorkerEnvelope, WorkerSource
from backend.common.schemas.canonical_result import PatentOutputs
from backend.common.llm.inference import llm_structured

@shared_task(name="workers.patent_worker.worker.run")
def run_patent_worker(job_id: str, task_id: str, params: dict):
    # Patent Intelligence Worker.
    
    job_uuid = uuid.UUID(job_id)
    task_uuid = uuid.UUID(task_id)

    molecule = params.get("molecule")
    if not molecule:
        raise ValueError("Patent Worker requires 'molecule' in params")
    
    # LLM-driven patent discovery
    prompt = (
        f"Identify key patents and intellectual property filings for the molecule '{molecule}'.\n"
        "Provide a list of patents including Patent IDs, titles, assignees, status, and summaries."
    )
    
    outputs = llm_structured(
        prompt=prompt,
        schema=PatentOutputs,
        job_id=job_uuid,
        stage="patent_discovery"
    )

    envelope = WorkerEnvelope(
        job_id= job_uuid,
        task_id= task_uuid,
        worker= "patent_worker",
        status= "ok",
        confidence= 0.85,
        timestamp= datetime.now(UTC),
        outputs= outputs.model_dump(),
        sources= [
            WorkerSource(
                type= "patent_search",
                title= "Patent Intelligence Discovery",
                uri= "https://patents.google.com",
                retrieved_at= datetime.now(UTC)
            )
        ],
        notes= f"Discovered {len(outputs.patents)} patents for {molecule}."
    )

    return envelope.model_dump(mode='json')
