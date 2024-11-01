from abc import ABC, abstractmethod

from dto.site_request.site_request_decline_dto import SiteRequestDeclineDto
from dto.site_request.site_request_request_dto import SiteRequestRequestDto
from dto.site_request.site_request_update_request_dto import SiteRequestUpdateRequestDto
from entities.site_request import SiteRequest
from handlers.pagination.response_pagination_handler import ResponsePaginationHandler

class ISiteRequestService(ABC):
    @abstractmethod
    def get_all(self, search: str, page: int, limit: int, order_by: int,
                column_name: str) -> ResponsePaginationHandler | None:
        pass

    @abstractmethod
    def get_by_account(self, account: str, search: str, page: int, limit: int, order_by: int,
                       column_name: str) -> ResponsePaginationHandler | None:
        pass

    @abstractmethod
    def get_by_guid(self, guid: str) -> SiteRequest | None:
        pass

    @abstractmethod
    def create_request(self, request: SiteRequestRequestDto) -> SiteRequest | None:
        pass

    @abstractmethod
    def update_request(self, update_request: SiteRequestUpdateRequestDto) -> int:
        pass

    @abstractmethod
    def accept(self, guid: str) -> int:
        pass

    @abstractmethod
    def decline(self, decline_request: SiteRequestDeclineDto) -> int:
        pass

    @abstractmethod
    def delete_request(self, guid: str) -> int:
        pass