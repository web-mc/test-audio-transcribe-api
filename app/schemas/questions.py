from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1, description="Вопрос пользователя по расшифровке"
    )


class QuestionResponse(BaseModel):
    transcription_id: int = Field(description="ID расшифровки")
    question: str = Field(description="Исходный вопрос")
    answer: str = Field(description="Ответ от ИИ")
