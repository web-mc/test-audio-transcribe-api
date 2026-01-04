import asyncio
from typing import Any

from celery import Task


class AsyncTask(Task):
    """Базовый класс для запуска асинхронных задач в Celery."""

    def __call__(self, *args, **kwargs)  -> Any:
        # Используем существующий цикл или создаем новый
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return loop.create_task(self.run(*args, **kwargs))
        return loop.run_until_complete(self.run(*args, **kwargs))
