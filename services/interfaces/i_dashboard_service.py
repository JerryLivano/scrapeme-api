from abc import ABC, abstractmethod
from dto.dashboard.count_dto import CountDto
from dto.dashboard.scrape_statistic_response_dto import ScrapeStatisticResponseDto
from dto.dashboard.top_scraper_response_dto import TopScraperResponseDto
from entities.user import User


class IDashboardService(ABC):
    @abstractmethod
    def get_dashboard_count(self) -> CountDto | None:
        pass

    @abstractmethod
    def get_user_by_account(self, account_guid: str) -> User | None:
        pass

    @abstractmethod
    def get_top_scraper(self) -> list[TopScraperResponseDto] | None:
        pass

    @abstractmethod
    def get_site_name(self, site_guid: str) -> str | None:
        pass

    @abstractmethod
    def get_scrape_statistic(self) -> list[ScrapeStatisticResponseDto] | None:
        pass