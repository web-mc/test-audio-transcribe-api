# -*- coding: utf-8 -*-
import logging
from functools import cached_property
from pathlib import Path
from socket import gethostbyname, gethostname
from typing import Annotated

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )


class AppSettings(BaseConfig):
    app_dir: Path = Path(__file__).parents[2]
    log_dir: Path = Path(__file__).parents[1] / "logs"
    production: Annotated[bool, Field(default=False)]

    allowed_extensions: Annotated[tuple, Field(default=(".mp3", ".wav"))]
    max_file_size: Annotated[int, Field(default=25 * 1024 * 1024)]  # 25 MB

    @property
    def loglevel(self) -> int:
        return logging.INFO if self.production else logging.DEBUG


app_settings = AppSettings()  # type: ignore


class GunicornSettings(BaseConfig):
    hostname: str = gethostname()
    host: str = gethostbyname(hostname)
    port: Annotated[int, Field(alias="API_PORT", default=8000)]
    reload: bool = not app_settings.production


gunicorn_settings = GunicornSettings()  # type: ignore


class DatabaseSettings(BaseConfig):
    user: Annotated[str, Field(default="postgres")]
    password: Annotated[SecretStr, Field(default=SecretStr("postgres"))]
    host: Annotated[str, Field(default="localhost")]
    port: Annotated[int, Field(default=5432)]
    db_schema: Annotated[str, Field(alias="POSTGRES_SCHEMA", default="public")]
    db_name: Annotated[str, Field(alias="POSTGRES_DB", default="postgres")]

    @cached_property
    def conn_string(cls) -> URL:
        conn_string = URL.create(
            drivername="postgresql+asyncpg",
            username=cls.user,
            password=cls.password.get_secret_value(),
            database=cls.db_name,
            host=cls.host,
            port=cls.port,
        )

        return conn_string

    class Config:
        env_prefix = "POSTGRES_"


db_settings = DatabaseSettings()  # type: ignore


class RabbitMQSettings(BaseConfig):
    user: Annotated[str, Field(default="guest")]
    password: Annotated[SecretStr, Field(alias="RABBITMQ_DEFAULT_PASS", default=SecretStr("guest"))]
    vhost: Annotated[str, Field(default="vhost")]
    host: Annotated[str, Field(default="localhost")]
    port: Annotated[int, Field(default=5672)]

    @cached_property
    def broker_url(cls) -> str:
        return f"amqp://{cls.user}:{cls.password.get_secret_value()}@{cls.host}:{cls.port}/{cls.vhost}"

    class Config:
        env_prefix = "RABBITMQ_DEFAULT_"


rabbitmq_settings = RabbitMQSettings()  # type: ignore


result_backend = db_settings.conn_string._replace(drivername="db+postgresql")
