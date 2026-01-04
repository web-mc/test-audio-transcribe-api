from app.celery_app.celery_app import celery_app
from app.db import async_session_maker

from .async_task import AsyncTask


@celery_app.task(
    base=AsyncTask,
    name="transcribe_audio",
    bind=True,
    retry_backoff=3,
    max_retries=3,
)
async def transcribe_audio(self, transcription_id: int) -> None:
    from app.dependencies.transcriptions import (
        get_ai_client,
        get_transcription_service,
        get_transcriptions_repo,
        get_transcriptions_storage,
    )

    async with async_session_maker() as session:
        repo = get_transcriptions_repo(session)
        client = get_ai_client()
        storage = get_transcriptions_storage()

        service = get_transcription_service(repo, storage, client)

        try:
            await service.transcribe_audio(transcription_id)
        except Exception as exc:
            raise self.retry(exc=exc)
