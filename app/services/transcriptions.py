from pathlib import Path
from typing import Any

from celery import states
from fastapi import HTTPException, UploadFile, status

from app.ai_clients import AiClientABC
from app.celery_app.celery_app import celery_app
from app.celery_app.tasks.transcriptions import transcribe_audio
from app.repositories import TranscriptionsRepo
from app.storages.abс_storage import StorageABC


class TranscriptionService:
    def __init__(
        self,
        repo: TranscriptionsRepo,
        storage: StorageABC,
        ai_client: AiClientABC,
    ) -> None:
        self.repo = repo
        self.storage = storage
        self.ai_client = ai_client

    async def process_audio(self, audio_file: UploadFile) -> dict[str, Any]:
        # 1 Сохраняем в хранилище
        file_path = await self.storage.save_audio(audio_file)

        # 2 записываем в БД данные файла
        async with self.repo.session.begin():
            tid = await self.repo.add_one({"file_path": file_path})

        # 3 Запускем селери задачу, передать IDшники файла в БД и задания
        transcribe_audio.apply_async(  # type: ignore
            kwargs={"transcription_id": tid},
            task_id=f"transcribe:{tid}",
        )

        return {
            "transcription_id": tid,
            "status": "STARTED",
        }

    async def get_transcription(self, tid: int) -> dict[str, str]:
        # 1 Провряем есть ли запись в БД
        async with self.repo.session.begin():
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

    async def delete_transcription(self, tid: int) -> int | None:
        async with self.repo.session.begin():
            audio = await self.repo.find_one(id=tid)
            res = await self.repo.delete_one(id=tid)
            self.storage.delete_audio(audio.file_path)  # type: ignore[union-attr]
            return res

    async def transcribe_audio(self, tid: int) -> None:
        # 1 получаем данные по ID БД, если там есть расшифровка уже, то завершаем таску
        async with self.repo.session.begin():
            audio = await self.repo.find_one(id=tid)
            if not audio or audio.transcription:
                return

        # 2 Отправляем запрос в Сервис расшифровки на расшифровку аудио
        transcription = await self.ai_client.process_audio(Path(audio.file_path))

        # 3 Записываем расшифровку в БД
        async with self.repo.session.begin():
            data = {"transcription": transcription}
            await self.repo.update_one(audio.id, data)  # type: ignore[attr-defined]

    async def ask_question(self, tid: int, question: str) -> str | None:
        async with self.repo.session.begin():
            audio = await self.repo.find_one(id=tid)

        if not audio or not audio.transcription:
            return "Аудио отуствует или расшифровка не готова."

        answer = await self.ai_client.ask_question(question, audio.transcription)
        return answer
