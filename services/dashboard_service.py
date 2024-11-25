from pymongo.errors import PyMongoError
from dto.dashboard.count_dto import CountDto
from dto.dashboard.top_scraper_response_dto import TopScraperResponseDto
from repositories.account_repository import AccountRepository
from repositories.scrape_data_repository import ScrapeDataRepository
from repositories.site_repository import SiteRepository
from repositories.site_request_repository import SiteRequestRepository


class DashboardService:
    def __init__(self, db):
        self._account_repository = AccountRepository(db)
        self._site_repository = SiteRepository(db)
        self._request_repository = SiteRequestRepository(db)
        self._scrape_repository = ScrapeDataRepository(db)

    def get_dashboard_count(self) -> CountDto | None:
        try:
            result = CountDto(
                self._account_repository.get_count(),
                self._site_repository.get_count(),
                self._request_repository.get_count()
            )
            return result
        except PyMongoError:
            return None

    def get_top_scraper(self) -> list[TopScraperResponseDto] | None:
        try:
            result = self._scrape_repository.get_top_scraper()
            if not result:
                return None
            return [TopScraperResponseDto(

            ) for data in result]
        except PyMongoError:
            return None
