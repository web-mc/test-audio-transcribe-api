from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from .base_sqlalchemy_repo import SQLAlchemyRepository


class TranscriptionsRepo(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession, model: type[DeclarativeBase]) -> None:
        super().__init__(session, model)
