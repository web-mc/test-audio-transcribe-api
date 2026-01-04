from abc import ABC, abstractmethod

from fastapi import UploadFile


class StorageABC(ABC):
    @abstractmethod
    async def save_audio(self, file: UploadFile) -> str:
        """
        Сохраняет загруженный аудиофайл в хранилище.

        Аргументы:
            file (UploadFile): Загружаемый файл.

        Возвращает:
            str: Путь к сохраненному файлу.
        """
        pass

    @abstractmethod
    def extract_filename_from_path(self, file_path: str) -> str:
        pass
