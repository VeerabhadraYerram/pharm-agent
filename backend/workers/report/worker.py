from celery_app import celery_app


@celery_app.task(name="workers.report.worker.ping")
def ping():
    return "pong from report worker"