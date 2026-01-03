from logging import getLogger
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.db import async_session_maker

from .abc_repo import AbstractRepository

logger = getLogger(__name__)


class SQLAlchemyRepository(AbstractRepository):
    model = None

    @classmethod
    async def add_one(cls, data: dict) -> int:
        try:
            query = insert(cls.model).values(data).returning(cls.model.id)  # type: ignore[arg-type,attr-defined]
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one()
        except (SQLAlchemyError, Exception) as e:
            msg = "невозможно вставить данные в таблицу"
            if isinstance(e, SQLAlchemyError):
                msg = f"Ошибка базы данных: {msg}."
            elif isinstance(e, Exception):
                msg = f"Неизвестная ошибка:  {msg}."

            logger.error(msg)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, msg)

    @classmethod
    async def find_one(cls, **filter_by) -> Any | None:
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(**filter_by)  # type: ignore[call-overload]
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    @classmethod
    async def delete_one(cls, **filter_by) -> int | None:
        try:
            async with async_session_maker() as session:
                stmt = delete(cls.model).filter_by(**filter_by).returning(cls.model.id)  # type: ignore[arg-type,attr-defined]
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one_or_none()

        except (SQLAlchemyError, Exception) as e:
            msg = "ошибка при удалнеии записи"
            if isinstance(e, SQLAlchemyError):
                msg = f"Ошибка базы данных: {msg}."
            elif isinstance(e, Exception):
                msg = f"Неизвестная ошибка:  {msg}."

            logger.error(msg)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, msg)
