from typing import Optional

from pydantic import BaseModel


class TranscriptionRead(BaseModel):
    transcription_id: int
    status: str
    file_name: str
    error: Optional[str] = None
    transcription: Optional[str] = None

    class Config:
        from_attributes = True
