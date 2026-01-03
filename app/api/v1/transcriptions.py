from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse, Response

from app.repositories import TranscriptionsRepo
from app.storages import LocalStorage

from .dependencies import validate_audio_file

transcriptions = APIRouter(
    prefix="/transcriptions",
    tags=["transcriptions"],
)


@transcriptions.post("/")
async def add_transcription(
    audio_file: UploadFile = Depends(validate_audio_file),
) -> JSONResponse:
    # 1 Сохраняем в хранилище
    file_path = await LocalStorage.save_audio(audio_file)

    # 2 записываем в БД данные файла
    transcription_id = await TranscriptionsRepo.add_one({"file_path": file_path})

    # 3 Запускем селери задачу, передать IDшники файла в БД и задания
    # 4 Возвращаем её ID клиенту в ответе и статус ACCEPTED

    return JSONResponse(
        content={"transcription_id": transcription_id},
        status_code=status.HTTP_202_ACCEPTED,
    )


@transcriptions.get("/{tid}")
async def get_transcription(tid: int) -> JSONResponse:
    """
    Получает конкретную расшифровку по ID.

    Args:
        tid (int): transcription_id
    """
    res = await TranscriptionsRepo.find_one(id=tid)
    if not res:
        return JSONResponse(
            content={"detail": "Transcription not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return JSONResponse(
        content={
            "transcription_id": res.id,
            "file_path": res.file_path,
        },
        status_code=status.HTTP_200_OK,
    )


@transcriptions.delete("/{tid}")
async def del_transcription(tid: int) -> Response:
    res = await TranscriptionsRepo.delete_one(id=tid)
    if res is None:
        return JSONResponse(
            content={"detail": "Transcription not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
