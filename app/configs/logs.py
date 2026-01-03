import logging

from app.configs import app_settings

app_settings.log_dir.mkdir(exist_ok=True, parents=True)


class ErrorFilter(logging.Filter):
    def filter(self, record) -> bool:
        if record.levelno >= logging.ERROR:
            return True
        return False


class InfoFilter(logging.Filter):
    def filter(self, record) -> bool:
        if record.levelno <= logging.WARNING:
            return True
        return False


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": app_settings.loglevel,
        "handlers": ["console", "error_file", "access_file"],
    },
    "loggers": {
        "gunicorn.error": {
            "level": app_settings.loglevel,
            "handlers": ["console", "error_file", "access_file"],
            "propagate": False,
        },
        "gunicorn.access": {
            "propagate": False,
            "level": app_settings.loglevel,
            "handlers": ["console", "access_file", "error_file"],
        },
        "uvicorn.error": {
            "level": app_settings.loglevel,
            "handlers": ["console", "error_file", "access_file"],
            "propagate": False,
        },
        "uvicorn.access": {
            "propagate": False,
            "level": app_settings.loglevel,
            "handlers": ["console", "access_file", "error_file"],
        },
    },
    "handlers": {
        "console": {
            "level": app_settings.loglevel,
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": "ext://sys.stdout",
        },
        "error_file": {
            "level": logging.ERROR,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "generic",
            "filename": app_settings.log_dir / "errors.log",
            "mode": "a+",
            "backupCount": 3,
            "maxBytes": 5_000_000,
            "encoding": "utf-8",
            "filters": ["error_filter"],
        },
        "access_file": {
            "level": app_settings.loglevel,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "generic",
            "filename": app_settings.log_dir / "info.log",
            "mode": "a+",
            "backupCount": 3,
            "maxBytes": 5_000_000,
            "encoding": "utf-8",
            "filters": ["info_filter"],
        },
    },
    "formatters": {
        "generic": {
            "format": "%(asctime)s | %(name)s | [%(levelname)s] %(message)s",
        },
    },
    "filters": {
        "error_filter": {
            "()": ErrorFilter,
        },
        "info_filter": {
            "()": InfoFilter,
        },
    },
}
