from celery import Celery

from app.configs import db_settings as db
from app.configs import rabbitmq_settings

result_backend = db.conn_string._replace(drivername="db+postgresql")

celery_app = Celery(
    "celery_app",
    broker_url=rabbitmq_settings.broker_url,
    result_backend=result_backend.render_as_string(False),
    include=[
        "app.celery_app.tasks.transcriptions",
    ],
)
