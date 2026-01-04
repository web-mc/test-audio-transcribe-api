from typing import Any

from celery import states
from fastapi import HTTPException, UploadFile, status

from app.celery_app.celery_app import celery_app
from app.celery_app.tasks.transcriptions import transcribe_audio
from app.repositories import TranscriptionsRepo
from app.storages.abс_storage import StorageABC


class TranscriptionService:
    def __init__(self, repo: TranscriptionsRepo, storage: StorageABC) -> None:
        self.repo = repo
        self.storage = storage

    async def process_audio(self, audio_file: UploadFile) -> dict[str, Any]:
        # 1 Сохраняем в хранилище
        file_path = await self.storage.save_audio(audio_file)

        # 2 записываем в БД данные файла
        tid = await self.repo.add_one({"file_path": file_path})

        # 3 Запускем селери задачу, передать IDшники файла в БД и задания
        transcribe_audio.apply_async(
            kwargs={
                "file_path": file_path,
                "transcription_id": tid,
            },
            task_id=f"transcribe:{tid}",
        )

        return {
            "transcription_id": tid,
            "status": "STARTED",
        }

    async def get_transcription(self, tid: int) -> dict[str, str]:
        # 1 Провряем есть ли запись в БД
        audio = await self.repo.find_one(id=tid)
        if not audio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transcription not found",
            )

        # 2 проверяем статус селери
        task = celery_app.AsyncResult(f"transcribe:{tid}")
        state = task.state

        result = {
            "transcription_id": tid,
            "status": state,
            "file_name": self.storage.extract_filename_from_path(audio.file_path),
        }

        if state in (states.PENDING, states.STARTED):
            return result

        if state == states.FAILURE:
            result["error"] = str(task.result)
            return result

        result["transcription"] = audio.transcription
        return result
