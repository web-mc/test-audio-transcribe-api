from logging import getLogger
from typing import Any, Type

from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from .abc_repo import AbstractRepository

logger = getLogger(__name__)


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession, model: Type[DeclarativeBase]) -> None:
        self.session = session
        self.model = model

    async def add_one(self, data: dict) -> int:
        try:
            query = insert(self.model).values(data).returning(self.model.id)  # type: ignore[attr-defined]
            async with self.session.begin():
                result = await self.session.execute(query)
                await self.session.commit()
                return result.scalar_one()
        except (SQLAlchemyError, Exception) as e:
            msg = "невозможно вставить данные в таблицу"
            if isinstance(e, SQLAlchemyError):
                msg = f"Ошибка базы данных: {msg}."
            elif isinstance(e, Exception):
                msg = f"Неизвестная ошибка:  {msg}."

            logger.error(msg)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, msg)

    async def find_one(self, **filter_by) -> Any | None:
        async with self.session.begin():
            stmt = select(self.model).filter_by(**filter_by)
            res = await self.session.execute(stmt)
            return res.scalar_one_or_none()

    async def delete_one(self, **filter_by) -> int | None:
        try:
            async with self.session.begin():
                stmt = (
                    delete(self.model).filter_by(**filter_by).returning(self.model.id)  # type: ignore[attr-defined]
                )
                result = await self.session.execute(stmt)
                await self.session.commit()
                return result.scalar_one_or_none()

        except (SQLAlchemyError, Exception) as e:
            msg = "ошибка при удалнеии записи"
            if isinstance(e, SQLAlchemyError):
                msg = f"Ошибка базы данных: {msg}."
            elif isinstance(e, Exception):
                msg = f"Неизвестная ошибка:  {msg}."

            logger.error(msg)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, msg)
