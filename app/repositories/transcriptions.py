from app.models import Transcriptions

from .base_sqlalchemy_repo import SQLAlchemyRepository


class TranscriptionsRepo(SQLAlchemyRepository):
    model = Transcriptions  # type: ignore[assignment]
