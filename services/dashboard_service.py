from pymongo.errors import PyMongoError
from dto.dashboard.count_dto import CountDto
from repositories.account_repository import AccountRepository
from repositories.site_repository import SiteRepository
from repositories.site_request_repository import SiteRequestRepository


class DashboardService:
    def __init__(self, db):
        self._account_repository = AccountRepository(db)
        self._site_repository = SiteRepository(db)
        self._request_repository = SiteRequestRepository(db)

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
