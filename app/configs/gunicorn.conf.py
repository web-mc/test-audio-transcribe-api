import multiprocessing

from app.configs import LOGGING_CONFIG, app_settings, gunicorn_settings

proc_name = "fastapi"

bind = f"{gunicorn_settings.host}:{gunicorn_settings.port}"

access_log_format = '%({x-forwarded-for}i)s %(t)s "%(r)s" %(s)s "%(a)s" %(L)s'
loglevel = "info" if app_settings.production else "debug"

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2 + 1 if app_settings.production else 2
reload = gunicorn_settings.reload

logconfig_dict = LOGGING_CONFIG
