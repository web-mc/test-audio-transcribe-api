from abc import ABC, abstractmethod
from typing import Any


class AbstractRepository(ABC):
    @classmethod
    @abstractmethod
    async def add_one(cls, data: dict) -> int:
        pass

    @classmethod
    @abstractmethod
    async def find_one(cls, **filter_by) -> Any | None:
        pass

    @classmethod
    @abstractmethod
    async def delete_one(cls, **filter_by) -> int | None:
        pass
