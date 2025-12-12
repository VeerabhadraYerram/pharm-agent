from celery import Celery


celery_app = Celery(
    "pharm_agent",
    broker="redis://localhost:6380/0",
    backend="redis://localhost:6380/1",
)

# queue routing
celery_app.conf.update(
    task_routes={
        "workers.clinical_trials.worker.*": {"queue": "clinical_trials"},
        "workers.report.worker.*": {"queue": "report"},
    },
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)