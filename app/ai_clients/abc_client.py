from abc import ABC, abstractmethod


class AiClientABC(ABC):
    @abstractmethod
    async def process_audio(self, audio) -> str:
        """
        Получает на вход аудио файл и отправляет его на транскрибацию.
        Возвращает текстовую расшифровку.
        """

    @abstractmethod
    async def ask_question(self, question: str, trancription: str) -> str | None:
        """
        Получает ответ на вопрос пользователя по заданному тексту.
        """
