import uuid
from datetime import datetime, UTC
from celery import shared_task

from backend.common.schemas.worker_envelope import WorkerEnvelope, WorkerSource
from backend.common.schemas.worker_outputs import MarketIntelligenceOutputs
from backend.common.tools.web_search import search_market_info
from backend.common.llm.inference import llm_structured

@shared_task(name="workers.market_worker.worker.run")
def run_market_worker(job_id: str, task_id: str, params: dict):
    # Market & Competitor Intelligence Worker.
    # Uses real-time web search and LLM synthesis.
    
    job_uuid = uuid.UUID(job_id)
    task_uuid = uuid.UUID(task_id)

    molecule = params.get("molecule")
    if not molecule:
        raise ValueError("Market Worker requires 'molecule' in params")

    # 1. Search for live data
    search_results = search_market_info(molecule)
    
    # 2. Synthesize with LLM
    prompt = (
        f"Analyze the following search results for the pharmaceutical molecule '{molecule}'.\n"
        "Extract key market intelligence, including market size, primary competitors, patent status, and pricing insights.\n\n"
        "Search Results:\n"
        f"{search_results}"
    )
    
    outputs = llm_structured(
        prompt=prompt,
        schema=MarketIntelligenceOutputs,
        job_id=job_uuid,
        stage="market_analysis"
    )

    envelope = WorkerEnvelope(
        job_id= job_uuid,
        task_id= task_uuid,
        worker= "market_worker",
        status= "ok",
        confidence= 0.85,
        timestamp= datetime.now(UTC),
        outputs= outputs.model_dump(),
        sources= [
            WorkerSource(
                type="web_search",
                title=f"Market Intelligence Search for {molecule}",
                uri="duckduckgo://search",
                retrieved_at=datetime.now(UTC)
            )
        ],
        notes=f"Synthesized market data for {molecule} from web search results."
    )

    return envelope.model_dump(mode='json')
