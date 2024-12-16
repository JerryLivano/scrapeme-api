from abc import ABC, abstractmethod
from dto.scrape_data.scrape_data_request_dto import ScrapeDataRequestDto
from dto.scrape_data.update_fav_dto import UpdateFavDto
from dto.scrape_data.update_name_dto import UpdateNameDto
from dto.scrape_data.update_note_dto import UpdateNoteDto
from entities.scrape_data import ScrapeData
from handlers.pagination.response_pagination_handler import ResponsePaginationHandler


class IScrapeDataService(ABC):
    @abstractmethod
    def get_by_account(self, account_guid: str, search: str, page: int, limit: int, order_by: int,
                       column_name: str, site_guid: str | None) -> ResponsePaginationHandler | None:
        pass

    @abstractmethod
    def create_scrape_data(self, request: ScrapeDataRequestDto) -> ScrapeData | None:
        pass

    @abstractmethod
    def get_all_web_data(self, guid: str, search: str, page: int, limit: int, order_by: int,
                         column_name: str) -> ResponsePaginationHandler | None:
        pass

    @abstractmethod
    def get_fav_scrape_data(self, account_guid: str, search: str, page: int, limit: int, order_by: int,
                            column_name: str, site_guid: str | None) -> ResponsePaginationHandler | None:
        pass

    @abstractmethod
    def get_all_fav_web_data(self, guid: str, search: str, page: int, limit: int, order_by: int,
                             column_name: str) -> ResponsePaginationHandler | None:
        pass

    @abstractmethod
    def update_fav(self, request: UpdateFavDto) -> int:
        pass

    @abstractmethod
    def update_note(self, request: UpdateNoteDto) -> int:
        pass

    @abstractmethod
    def update_scrape(self, request: UpdateNameDto) -> bool:
        pass

    @abstractmethod
    def delete_scrape(self, guid: str) -> bool:
        pass