from abc import ABC, abstractmethod

class IRoleRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_guid(self, guid: str):
        pass

    @abstractmethod
    def create(self, role):
        pass

    @abstractmethod
    def update(self, role):
        pass

    @abstractmethod
    def delete(self, guid: str):
        pass