from celery import Celery
from dotenv import load_dotenv
import os


load_dotenv()

celery_app = Celery(
    "pharm_agent",
    broker=os.getenv("REDIS_BROKER_URL"),
    backend=os.getenv("REDIS_BACKEND_URL"),
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