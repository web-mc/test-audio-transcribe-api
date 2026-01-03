from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @classmethod
    @abstractmethod
    async def add_one(cls, data: dict) -> int:
        pass
