from fastapi import Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs import app_settings
from app.db import get_async_session
from app.models import Transcriptions
from app.repositories.transcriptions import TranscriptionsRepo
from app.services.transcriptions import TranscriptionService
from app.storages import LocalStorage
from app.storages.abс_storage import StorageABC


async def validate_audio_file(
    audio_file: UploadFile = File(
        description=(
            f"Allowed extensions: {', '.join(app_settings.allowed_extensions)}. "
            f"Max size: {app_settings.max_file_size // (1024 * 1024)} MB."
        ),
        examples=["example.mp3"],
    ),
) -> UploadFile:
    if not audio_file.filename:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Filename is required")

    if not audio_file.filename.lower().endswith(app_settings.allowed_extensions):
        raise HTTPException(415, "Unsupported file type")

    if audio_file.size is not None and audio_file.size > app_settings.max_file_size:
        raise HTTPException(status.HTTP_413_CONTENT_TOO_LARGE, "File too large")

    return audio_file


def get_transcriptions_repo(
    session: AsyncSession = Depends(get_async_session),
) -> TranscriptionsRepo:
    return TranscriptionsRepo(session, Transcriptions)


def get_transcriptions_storage() -> StorageABC:
    return LocalStorage()


def get_transcription_service(
    repo: TranscriptionsRepo = Depends(get_transcriptions_repo),
    storage: StorageABC = Depends(get_transcriptions_storage),
) -> TranscriptionService:
    return TranscriptionService(repo, storage)
