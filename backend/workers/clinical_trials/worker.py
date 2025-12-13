import json
import uuid
import uuid6
from datetime import datetime, UTC
from pathlib import Path

from celery import shared_task

from backend.common.schemas.worker_envelope import WorkerEnvelope, WorkerSource
from backend.common.schemas.worker_outputs import ClinicalTrialsOutputs
from backend.common.schemas.canonical_result import TrialRecord


DATASET_PATH = Path(__file__).parents[2] / "mocks" / "clinical_trials.json"

# WARNING TO SELF - DONT DO THIS WHEN DATASET IS BIG (E.G., LIVE API)
def _load_dataset():
    if not DATASET_PATH.exists():
        return []
    with open(DATASET_PATH, "r") as f:
        return json.load(f)

GLOBAL_DATASET = _load_dataset()

def filter_trials(dataset: list[dict], molecule: str) -> list[dict]:
    # Filter trials containing molecule name in relevant fields.
    molecule_lower = molecule.lower()

    def matches(entry: dict) -> bool:
        fields = [
            entry.get("intervention", ""),
            entry.get("condition", ""),
            entry.get("title", ""),
        ]
        combined = " ".join([str(f).lower() for f in fields])

        return molecule_lower in combined
    return [e for e in dataset if matches(e)]

def normalize_trial(raw: dict) -> TrialRecord:
    # normalize raw json into TrialRecord schema
    return TrialRecord(
        nct_id=raw.get("nct_id", ""),
        phase=raw.get("phase", ""),
        status=raw.get("status", ""),
        condition=raw.get("condition", ""),
        region=raw.get("region"),
        results_summary=raw.get("results_summary")
    )

@shared_task(name="workers.clinical_trials.worker.run")
def run_clinical_trials_worker(job_id: str, task_id: str, params: dict):
    # CT Worker. Produces structured evidence
    
    job_uuid = uuid.UUID(job_id)
    task_uuid = uuid.UUID(task_id)

    molecule = params.get("molecule")
    if not molecule:
        raise ValueError("Clinical Trials Worker requires 'molecule' in params")
    
    filtered = filter_trials(GLOBAL_DATASET, molecule)
    normalized = [normalize_trial(e) for e in filtered]

    outputs = ClinicalTrialsOutputs(
        trials=normalized,
        summary_text="",
        research_confidence=0.0,
        key_findings=[],
        suggested_follow_up=[]
    )

    envelope = WorkerEnvelope(
        job_id= job_uuid,
        task_id= task_uuid,
        worker= "clinical_trials",
        status= "ok",
        confidence= 1.0,
        timestamp= datetime.now(UTC),
        outputs= outputs.model_dump(),
        sources= [
            WorkerSource(
                type= "dataset",
                title= "Mock Clinical Trials Dataset",
                uri= str(DATASET_PATH),
                retrieved_at= datetime.now(UTC)
            )
        ],
        notes= "Testing Testing 1 2 3 4 3 2 1 2 3"
    )

    return envelope.model_dump(mode='json')