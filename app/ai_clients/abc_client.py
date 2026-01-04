from abc import ABC, abstractmethod
from pathlib import Path


class AiClientABC(ABC):
    @abstractmethod
    async def process_audio(self, audio_path: Path) -> str:
        """
        Получает на вход аудио файл и отправляет его на транскрибацию.
        Возвращает текстовую расшифровку.
        """

    @abstractmethod
    async def ask_question(self, question: str, transcription: str) -> str | None:
        """
        Получает ответ на вопрос пользователя по заданному тексту.
        """
