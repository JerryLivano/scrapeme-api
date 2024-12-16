from pymongo.errors import PyMongoError
from dto.dashboard.count_dto import CountDto
from dto.dashboard.scrape_statistic_response_dto import ScrapeStatisticResponseDto
from dto.dashboard.top_scraper_response_dto import TopScraperResponseDto
from entities.user import User
from repositories.account_repository import AccountRepository
from repositories.scrape_data_repository import ScrapeDataRepository
from repositories.site_repository import SiteRepository
from repositories.site_request_repository import SiteRequestRepository
from repositories.user_repository import UserRepository
from services.interfaces.i_dashboard_service import IDashboardService


class DashboardService(IDashboardService):
    def __init__(self, db):
        self._account_repository = AccountRepository(db)
        self._user_repository = UserRepository(db)
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

    def get_user_by_account(self, account_guid: str) -> User | None:
        try:
            user = self._account_repository.get_user_by_account(account_guid)
            if not user:
                return None
            result = self._user_repository.get_by_guid(user)
            return result
        except PyMongoError:
            return None

    def get_top_scraper(self) -> list[TopScraperResponseDto] | None:
        try:
            result = self._scrape_repository.get_top_scraper()
            if not result:
                return None
            result = [TopScraperResponseDto(
                name=self.get_user_by_account(data.account_guid).first_name + " " + self.get_user_by_account(
                    data.account_guid).last_name,
                email=self.get_user_by_account(data.account_guid).email,
                count=data.count
            ) for data in result]
            return result
        except PyMongoError:
            return None

    def get_site_name(self, site_guid: str) -> str | None:
        try:
            site = self._site_repository.get_by_guid(site_guid)
            if not site:
                return None
            return site.site_name
        except PyMongoError:
            return None

    def get_scrape_statistic(self) -> list[ScrapeStatisticResponseDto] | None:
        try:
            result = self._scrape_repository.get_scrape_statistic()
            if not result:
                return None
            return [ScrapeStatisticResponseDto(
                site_name=self.get_site_name(data.site_guid),
                count=data.count
            ) for data in result]
        except PyMongoError:
            return None
