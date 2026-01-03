import logging

from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse

from .dependencies import validate_audio_file

transcriptions = APIRouter(
    prefix="/transcriptions",
    tags=["transcriptions"],
)


@transcriptions.post("/")
def add_transcription(
    audio_file: UploadFile = Depends(validate_audio_file),
) -> JSONResponse:
    # 1 Сохраняем в хранилище
    # 2 записываем в БД данные файла
    # 3 Запускем селери задачу, передать IDшники файла в БД и задания
    # 4 Возвращаем её ID клиенту в ответе и статус ACCEPTED

    return JSONResponse(
        content={"file": audio_file.filename},
        status_code=status.HTTP_202_ACCEPTED,
    )


@transcriptions.get("/{transcription_id}")
def get_transcribtion(transcription_id: int) -> dict[str, str]:
    1/0
    return {"transcribe": "transcribe"}
