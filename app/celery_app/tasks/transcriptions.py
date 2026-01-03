from app.celery_app.celery_app import celery_app


@celery_app.task(bind=True)
def transcribe_audio(self, transcription_id: int, file_path: str) -> None:
    task_id = self.request.id
