import asyncio
from app.tasks.celery_app import celery


def _run(coro):
    """Run an async function from sync Celery task."""
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(coro)
    finally:
        loop.close()


@celery.task(name="app.tasks.jobs.job_ingest")
def job_ingest():
    from app.services.ingestion import run_all_ingestors
    _run(run_all_ingestors())


@celery.task(name="app.tasks.jobs.job_compute_ipi")
def job_compute_ipi():
    from app.services.forecasting import compute_inflation_pressure_index
    _run(compute_inflation_pressure_index())


@celery.task(name="app.tasks.jobs.job_forecast")
def job_forecast():
    from app.services.forecasting import run_prophet_forecast
    _run(run_prophet_forecast())


@celery.task(name="app.tasks.jobs.job_alerts")
def job_alerts():
    from app.services.alert_engine import run_all_alert_checks
    _run(run_all_alert_checks())


@celery.task(name="app.tasks.jobs.job_stress")
def job_stress():
    from app.services.alert_engine import compute_stress_scores
    _run(compute_stress_scores())