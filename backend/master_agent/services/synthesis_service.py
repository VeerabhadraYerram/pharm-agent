import uuid
from sqlalchemy.orm import Session

from backend.master_agent.services.task_service import TaskService
from backend.master_agent.services.job_service import JobService
from backend.master_agent.synthesis.engine import run_synthesis
from backend.common.schemas.worker_outputs import ClinicalTrialsOutputs


class SynthesisService:
    # wrap synthesis engine to behave like a task

    @staticmethod
    def execute_synthesis(
        db: Session,
        task_id: uuid.UUID,
        job_id: uuid.UUID,
        molecule: str,
        ct_outputs: ClinicalTrialsOutputs
    ):
        # 1. mark task running 
        # 2. execute synthesis LLM engine
        # 3. write canonical result in jobs table
        # 4. mark task completed
        # 5. if task failed, mark failed.

        # 1.
        TaskService.mark_running(db, task_id)

        try:
            
            # 2.
            canonical_result = run_synthesis(
                job_id = job_id,
                molecule = molecule,
                ct_outputs = ct_outputs
            )

            # 3.
            JobService.update_canonical_result(
                db = db,
                job_id = job_id,
                canonical_json = canonical_result.model_dump(mode="json")
            )

            # 4.
            TaskService.mark_completed(db, task_id)

            return canonical_result
        
        except Exception as e:

            # 5.
            TaskService.mark_failed(db, task_id, str(e))
            raise
