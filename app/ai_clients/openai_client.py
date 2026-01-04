from logging import getLogger
from pathlib import Path
from typing import NoReturn

from openai import AsyncOpenAI, OpenAIError
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam

from .abc_client import AiClientABC

logger = getLogger(__name__)


class OpenAiClient(AiClientABC):
    def __init__(
        self,
        base_url: str,
        api_key: str,
        text_model: str,
        audio_model: str,
    ) -> None:
        self.base_url = base_url
        self.text_model = text_model
        self.audio_model = audio_model
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=self.base_url,
        )

    async def process_audio(self, audio_path: Path) -> str:
        """
        Получает на вход аудио файл и отправляет его на транскрибацию.
        Возвращает текстовую расшифровку.
        """
        try:
            transcription = await self.client.audio.transcriptions.create(
                model=self.audio_model,
                file=audio_path,
            )
            return transcription.text.strip()
        except Exception as e:
            self.__error_handler(e, "Ошибка при транскрибации аудио")

    async def ask_question(self, question: str, transcription: str) -> str | None:
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": transcription},
            {"role": "user", "content": question},
        ]
        try:
            completion: ChatCompletion = await self.client.chat.completions.create(
                model=self.text_model,
                messages=messages,
                temperature=0.3,
            )
            return completion.choices[0].message.content
        except Exception as e:
            self.__error_handler(e, "Ошибка при транскрибации аудио")

    def __error_handler(self, e: Exception, msg: str) -> NoReturn:
        if isinstance(e, OpenAIError):
            msg = f"Ошибка AI клиента: {msg}."
        elif isinstance(e, Exception):
            msg = f"Неизвестная ошибка:  {msg}."

        logger.error(msg)
        raise RuntimeError(msg) from e
