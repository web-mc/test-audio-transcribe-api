from abc import ABC, abstractmethod
from typing import Any

from fastapi import UploadFile


class StorageABC(ABC):
    @classmethod
    @abstractmethod
    async def save_audio(cls, file: UploadFile) -> str:
        """
        Сохраняет загруженный аудиофайл в хранилище.

        Аргументы:
            file (UploadFile): Загружаемый файл.

        Возвращает:
            str: Путь к сохраненному файлу.
        """
        pass
