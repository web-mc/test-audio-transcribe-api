from app.celery_app.celery_app import celery_app


@celery_app.task(bind=True, retry_backoff=5, max_retries=3)
def transcribe_audio(self, transcription_id: int, file_path: str) -> None:
    task_id = self.request.id
