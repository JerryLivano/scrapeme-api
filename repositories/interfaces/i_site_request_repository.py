from abc import ABC, abstractmethod
from entities.site_request import SiteRequest

class ISiteRequestRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[SiteRequest] | None:
        pass

    @abstractmethod
    def get_count(self) -> int:
        pass

    @abstractmethod
    def get_by_guid(self, guid: str) -> SiteRequest | None:
        pass

    @abstractmethod
    def create(self, request: SiteRequest) -> SiteRequest | None:
        pass

    @abstractmethod
    def update(self, request: SiteRequest) -> bool:
        pass

    @abstractmethod
    def done_status(self, guid: str) -> bool:
        pass

    @abstractmethod
    def delete(self, guid: str) -> bool:
        pass