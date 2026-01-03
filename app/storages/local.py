from pathlib import Path
from typing import Any

import aiofiles
from fastapi import UploadFile

from app.configs import app_settings

from .abс_storage import StorageABC


class LocalStorage(StorageABC):
    upload_dir: Path = app_settings.app_dir / "uploads"

    @classmethod
    async def save_audio(cls, file: UploadFile) -> str:

        if not cls.upload_dir.exists():
            cls.upload_dir.mkdir(parents=True)

        file_path = cls.upload_dir / file.filename  # type: ignore

        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        return str(file_path.resolve())
