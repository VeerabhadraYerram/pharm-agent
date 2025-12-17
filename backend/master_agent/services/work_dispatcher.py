from celery import Celery
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.master_agent.services.task_service import TaskService
from backend.workers.clinical_trials.worker import run_clinical_trials_worker
from backend.workers.report.worker import run_report_worker


class WorkerDispatcher:
    # handle dispatching celery workers for master agent

    @staticmethod
    def dispatch_clinical_trials(db: Session, task_id, job_id, params: dict):

        try:
            
            # 1. dispatch
            async_result = run_clinical_trials_worker.delay(
                str(job_id),
                str(task_id),
                params
            )
            return async_result
        
        except Exception as e:
            
            # 2. if redis down, mark failed immediately
            print(f"[Dispatcher] failed to dispatch Clinical Worker: {e}")
            TaskService.mark_failed(db, task_id, f"Broker Dispatch Error: {str(e)}")

            raise e
        
    @staticmethod
    def dispatch_report(db: Session, task_id, job_id, params: dict):


        try:
            async_result = run_report_worker.delay(
                str(job_id),
                str(task_id),
                params
            )
            return async_result
        
        except Exception as e:

            print(f"[Dispatcher] Failed to dispatch Report Worker: {e}")
            TaskService.mark_failed(db, task_id, f"Broker Dispatch Error: {str(e)}")

            raise e        