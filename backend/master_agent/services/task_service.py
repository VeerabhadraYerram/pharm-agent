import uuid6
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.master_agent.models.task import Task


class TaskService:
    # handle db operations for task lifecycle

    @staticmethod
    def create_task(db: Session, job_id, worker_type: str, params: dict | None = None) -> Task:
        task = Task(
            id = uuid6.uuid7(),
            job_id = job_id,
            worker_type = worker_type,
            params = params or {},
            status = "pending",
            retries = 0,
            priority = 0,
            depends_on = []
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return task
    
    @staticmethod
    def mark_running(db: Session, task_id) -> Task:
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        task.status = "running"
        task.started_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(task)

        return task
    
    @staticmethod
    def mark_completed(db: Session, task_id) -> Task:
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        task.status = "completed"
        task.finished_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(task)

        return task
    
    @staticmethod
    def mark_failed(db: Session, task_id, error_msg: str) -> Task:
        # new method to handle worker failures gracefully

        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        task.status = "failed"
        task.finished_at = datetime.now(timezone.utc)
        task.error_message = error_msg[:5000]

        db.commit()
        db.refresh(task)
        
        return task
    
    @staticmethod
    def get_task(db: Session, task_id) -> Task:
        return db.query(Task).filter(Task.id == task_id).first()