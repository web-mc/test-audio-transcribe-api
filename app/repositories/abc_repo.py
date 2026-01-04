from abc import ABC, abstractmethod
from typing import Any


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict) -> int:
        pass

    @abstractmethod
    async def find_one(self, **filter_by) -> Any | None:
        pass

    @abstractmethod
    async def delete_one(self, **filter_by) -> int | None:
        pass
