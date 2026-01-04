from pathlib import Path

import aiofiles
from fastapi import UploadFile

from app.configs import app_settings

from .abс_storage import StorageABC


class LocalStorage(StorageABC):
    def __init__(self) -> None:
        self.upload_dir: Path = app_settings.app_dir / "uploads"

    async def save_audio(self, file: UploadFile) -> str:
        if not self.upload_dir.exists():
            self.upload_dir.mkdir(parents=True)

        file_path = self.upload_dir / file.filename  # type: ignore

        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        return str(file_path.resolve())

    def extract_filename_from_path(self, file_path: str) -> str:
        return Path(file_path).name

    def delete_audio(self, file_path: str) -> None:
        Path(file_path).unlink(missing_ok=True)
