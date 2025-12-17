import time
from sqlalchemy.orm import Session

from backend.master_agent.models.worker_response import WorkerResponse
from backend.common.schemas.worker_envelope import WorkerEnvelope


class ResponseWaiter:
    # polls db until worker response available/

    @staticmethod
    def wait_for_response(
        db: Session,
        task_id,
        poll_interval: float = 1.0,
        timeout_seconds: int = 30
    ) -> WorkerEnvelope:
        # blocks until worker writes a WorkerResponse row. 
        # Returns validated WorkerEnvelope obj

        start_time = time.time()

        while True:
            resp = (
                db.query(WorkerResponse)
                .filter(WorkerResponse.task_id == task_id)
                .first()
            )

            if resp:
                
                # parse db json using pydantic schema
                envelope = WorkerEnvelope.model_validate(resp.raw_envelope)
                return envelope
            
            if time.time() - start_time > timeout_seconds:
                raise TimeoutError(
                    f"Timed out waiting for worker response for task {task_id}"
                )
            
            time.sleep(poll_interval)