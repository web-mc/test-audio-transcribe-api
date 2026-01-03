# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from socket import gethostbyname, gethostname
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )


class AppSettings(BaseConfig):
    app_dir: Path = Path(__file__).parents[1]
    log_dir: Path = app_dir / "logs"
    production: Annotated[bool, Field(default=False)]

    allowed_extensions: Annotated[tuple, Field(default=(".mp3", ".wav"))]
    max_file_size: Annotated[int, Field(default=10 * 1024 * 1024)]  # 10 MB

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
