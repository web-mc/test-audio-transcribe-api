from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse, Response

from app.dependencies.transcriptions import (
    get_transcription_service,
    validate_audio_file,
)
from app.schemas.questions import QuestionRequest, QuestionResponse
from app.schemas.transcriptions import TranscriptionRead
from app.services.transcriptions import TranscriptionService

transcriptions = APIRouter(
    prefix="/transcriptions",
    tags=["Transcriptions"],
)


@transcriptions.post("/", summary="Отправить аудио на транскрибацию.")
async def add_transcription(
    audio_file: UploadFile = Depends(validate_audio_file),
    service: TranscriptionService = Depends(get_transcription_service),
) -> JSONResponse:
    content = await service.process_audio(audio_file)
    return JSONResponse(
        content=content,
        status_code=status.HTTP_202_ACCEPTED,
    )


@transcriptions.get(
    "/{tid}",
    response_model=TranscriptionRead,
    status_code=status.HTTP_200_OK,
    summary="Получить статус и результат транскрибации по ID.",
)
async def get_transcription(
    tid: int,
    service: TranscriptionService = Depends(get_transcription_service),
) -> dict[str, str]:
    transcription = await service.get_transcription(tid)
    return transcription


@transcriptions.delete("/{tid}", summary="Удалить расшифровку по ID.")
async def del_transcription(
    tid: int,
    service: TranscriptionService = Depends(get_transcription_service),
) -> Response:
    res = await service.delete_transcription(tid)
    if res is None:
        return JSONResponse(
            content={"detail": "Transcription not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@transcriptions.post(
    "/{tid}/questions",
    response_model=QuestionResponse,
    summary="Задать вопрос по содержанию аудио.",
)
async def ask_question(
    tid: int,
    question_body: QuestionRequest,
    service: TranscriptionService = Depends(get_transcription_service),
):
    answer = await service.ask_question(tid, question_body.question)
    return {
        "transcription_id": tid,
        "question": question_body.question,
        "answer": answer,
    }
