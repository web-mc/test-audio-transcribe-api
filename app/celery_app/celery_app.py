from celery import Celery

from app.configs import db_settings as db
from app.configs import rabbitmq_settings

result_backend = db.conn_string._replace(drivername="db+postgresql")

celery_app = Celery(
    "celery_app",
    broker_url=rabbitmq_settings.broker_url,
    result_backend=result_backend.render_as_string(False),
    enable_utc=True,
    timezone="UTC",
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
    result_expires=86400,  # 24 часа хроним результаты
    include=[
        "app.celery_app.tasks.transcriptions",
    ],
)
