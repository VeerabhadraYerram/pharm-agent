from celery_app import celery_app


@celery_app.task(name="workers.clinical_trials.worker.ping")
def ping():
    return "pong from clinical_trials"