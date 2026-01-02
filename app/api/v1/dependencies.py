from fastapi import File, HTTPException, UploadFile, status

from app.configs import app_settings


async def validate_audio_file(
    audio_file: UploadFile = File(
        description=(
            f"Allowed extensions: {', '.join(app_settings.allowed_extensions)}. "
            f"Max size: {app_settings.max_file_size // (1024 * 1024)} MB."
        ),
        example="example.mp3",
    ),
) -> UploadFile:
    if not audio_file.filename:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Filename is required")

    if not audio_file.filename.lower().endswith(app_settings.allowed_extensions):
        raise HTTPException(415, "Unsupported file type")

    if audio_file.size is not None and audio_file.size > app_settings.max_file_size:
        raise HTTPException(status.HTTP_413_CONTENT_TOO_LARGE, "File too large")

    return audio_file
