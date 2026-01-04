from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.configs import db_settings

engine = create_async_engine(db_settings.conn_string.render_as_string(False))
session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

async def get_async_session():
    async with session_maker() as session:
        yield session
