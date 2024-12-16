from abc import ABC, abstractmethod

from dto.dashboard.scrape_statistic_dto import ScrapeStatisticDto
from dto.dashboard.top_scraper_dto import TopScraperDto
from dto.scrape_data.update_fav_dto import UpdateFavDto
from dto.scrape_data.update_name_dto import UpdateNameDto
from dto.scrape_data.update_note_dto import UpdateNoteDto
from entities.scrape_data import ScrapeData


class IScrapeDataRepository(ABC):
    @abstractmethod
    def get_top_scraper(self) -> list[TopScraperDto] | None:
        pass

    @abstractmethod
    def get_scrape_statistic(self) -> list[ScrapeStatisticDto] | None:
        pass

    @abstractmethod
    def get_by_account(self, account: str) -> list[ScrapeData] | None:
        pass

    @abstractmethod
    def get_by_guid(self, guid: str) -> ScrapeData | None:
        pass

    @abstractmethod
    def create(self, scrape_data: ScrapeData) -> ScrapeData | None:
        pass

    @abstractmethod
    def update_favourite(self, request: UpdateFavDto) -> bool:
        pass

    @abstractmethod
    def update_note(self, request: UpdateNoteDto) -> bool:
        pass

    @abstractmethod
    def update_name(self, request: UpdateNameDto) -> bool:
        pass

    @abstractmethod
    def delete(self, guid: str) -> bool:
        pass
