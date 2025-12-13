from sqlalchemy.orm import Session


def run_scheduler(db: Session) -> None:
    # stub
    """
    - Query db for tasks with "pending" status
    - check dependencies
    - celery tasks
    - update task state
    """
    pass