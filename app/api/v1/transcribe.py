from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse

from .dependencies import validate_audio_file

transcribe = APIRouter(
    prefix="/transcribe",
    tags=["transcriber"],
)


@transcribe.post("/")
def transcribe_audio(
    audio_file: UploadFile = Depends(validate_audio_file),
) -> JSONResponse:
    return JSONResponse(
        content={"file": audio_file.filename},
        status_code=status.HTTP_202_ACCEPTED,
    )


@transcribe.get("/{id}")
def get_transcribtion(id: int) -> dict[str, str]:
    return {"transcribe": "transcribe"}
