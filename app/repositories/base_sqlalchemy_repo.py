from logging import getLogger

from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError

from app.db import async_session_maker

from .abc_repo import AbstractRepository

logger = getLogger(__name__)


class SQLAlchemyRepository(AbstractRepository):
    model = None

    @classmethod
    async def add_one(cls, data: dict) -> int:
        try:
            query = insert(cls.model).values(data).returning(cls.model.id)
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
            raise

    @classmethod
    async def find_one(cls, **filter_by):
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()
