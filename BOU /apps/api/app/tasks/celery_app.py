from celery import Celery
from app.core.config import settings

celery = Celery(
    "bou_sentinel",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Africa/Kampala",
    enable_utc=True,
    beat_schedule={
        "ingest-data-hourly": {
            "task": "app.tasks.jobs.job_ingest",
            "schedule": 3600.0,  # every 1 hour
        },
        "compute-ipi-every-6h": {
            "task": "app.tasks.jobs.job_compute_ipi",
            "schedule": 21600.0,  # every 6 hours
        },
        "run-forecast-daily": {
            "task": "app.tasks.jobs.job_forecast",
            "schedule": 86400.0,  # every 24 hours
        },
        "run-alerts-every-6h": {
            "task": "app.tasks.jobs.job_alerts",
            "schedule": 21600.0,
        },
        "compute-stress-daily": {
            "task": "app.tasks.jobs.job_stress",
            "schedule": 86400.0,
        },
    },
)