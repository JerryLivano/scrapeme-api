from abc import ABC, abstractmethod
from entities.account import Account

class IAccountRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Account] | None:
        pass

    @abstractmethod
    def get_count(self) -> int:
        pass

    @abstractmethod
    def get_by_guid(self, guid: str) -> Account | None:
        pass

    @abstractmethod
    def create(self, account: Account) -> Account | None:
        pass

    @abstractmethod
    def update(self, account: Account) -> Account | None:
        pass

    @abstractmethod
    def update_password(self, guid: str, changed_password: bytes) -> bool:
        pass

    @abstractmethod
    def delete(self, guid: str) -> bool:
        pass

    @abstractmethod
    def get_by_user_guid(self, guid: str) -> Account | None:
        pass