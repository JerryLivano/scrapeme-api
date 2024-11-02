from abc import ABC, abstractmethod
from dto.site.create_url_dto import CreateUrlDto
from dto.site.site_request_dto import SiteRequestDto
from dto.site.site_update_request_dto import SiteUpdateRequestDto
from entities.site import Site
from handlers.pagination.response_pagination_handler import ResponsePaginationHandler


class ISiteService(ABC):
    @abstractmethod
    def create_url(self, request: CreateUrlDto) -> str | None:
        pass

    @abstractmethod
    def get_all(self, search: str, page: int, limit: int, order_by: int, column_name: str) -> ResponsePaginationHandler | None:
        pass

    @abstractmethod
    def create_site(self, request: SiteRequestDto) -> Site | None:
        pass

    @abstractmethod
    def update_site(self, request: SiteUpdateRequestDto) -> int:
        pass

    @abstractmethod
    def delete_site(self, guid: str) -> int:
        pass