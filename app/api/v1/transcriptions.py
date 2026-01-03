from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse

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
    # 3 Запускем селери задачу, передать IDшники файла в БД и задания
    # 4 Возвращаем её ID клиенту в ответе и статус ACCEPTED

    return JSONResponse(
        content={"file_path": file_path},
        status_code=status.HTTP_202_ACCEPTED,
    )


@transcriptions.get("/{transcription_id}")
def get_transcription(transcription_id: int) -> dict[str, str]:
    return {"transcribe": "transcribe"}
