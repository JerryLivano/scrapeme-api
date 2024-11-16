from abc import ABC, abstractmethod
from entities.site import Site


class ISiteRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Site] | None:
        pass

    @abstractmethod
    def get_count(self) -> int:
        pass

    @abstractmethod
    def get_by_guid(self, guid: str) -> Site | None:
        pass

    @abstractmethod
    def create(self, site: Site) -> Site | None:
        pass

    @abstractmethod
    def update(self, site: Site) -> bool:
        pass

    @abstractmethod
    def delete(self, guid: str):
        pass