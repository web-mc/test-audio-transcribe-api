from logging import getLogger
from typing import Any, NoReturn, Type

from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select, update
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
            result = await self.session.execute(query)
            await self.session.flush()
            return result.scalar_one()
        except (SQLAlchemyError, Exception) as e:
            self.__error_handler(e, "невозможно вставить данные в таблицу")

    async def find_one(self, **filter_by) -> Any | None:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete_one(self, **filter_by) -> int | None:
        try:
            stmt = (
                delete(self.model).filter_by(**filter_by).returning(self.model.id)  # type: ignore[attr-defined]
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()

        except (SQLAlchemyError, Exception) as e:
            self.__error_handler(e, "ошибка при удалнеии записи")

    async def update_one(self, id: int, data: dict) -> None:
        try:
            query = (
                update(self.model)
                .where(self.model.id == id)  # type: ignore[attr-defined]
                .values(data)
            )
            await self.session.execute(query)

        except (SQLAlchemyError, Exception) as e:
            self.__error_handler(e, "ошибка при обновлении записи")

    def __error_handler(self, e: Exception, msg: str) -> NoReturn:
        if isinstance(e, SQLAlchemyError):
            msg = f"Ошибка базы данных: {msg}."
        elif isinstance(e, Exception):
            msg = f"Неизвестная ошибка:  {msg}."

        logger.error(msg)
        raise RuntimeError(msg) from e
