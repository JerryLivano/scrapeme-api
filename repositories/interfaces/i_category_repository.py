from abc import ABC, abstractmethod
from entities.category import Category

class ICategoryRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Category] | None:
        pass

    @abstractmethod
    def get_by_guid(self, guid: str) -> Category | None:
        pass

    @abstractmethod
    def create(self, category: Category) -> Category | None:
        pass

    @abstractmethod
    def update(self, category: Category) -> bool:
        pass

    @abstractmethod
    def delete(self, guid: str) -> bool:
        pass