from abc import ABC, abstractmethod
from entities.user import User

class IUserRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[User] | None:
        pass

    @abstractmethod
    def get_by_guid(self, guid: str) -> User | None:
        pass

    @abstractmethod
    def create(self, user: User) -> User | None:
        pass

    @abstractmethod
    def update(self, user: User) -> User | None:
        pass

    @abstractmethod
    def delete(self, guid: str) -> bool:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass