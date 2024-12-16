from datetime import datetime, timedelta
from uuid import uuid4
from pymongo.database import Database
from pymongo.errors import PyMongoError
from dto.scrape_data.get_scrape_dto import GetScrapeDto
from dto.scrape_data.scrape_data_request_dto import ScrapeDataRequestDto
from dto.scrape_data.update_fav_dto import UpdateFavDto
from dto.scrape_data.update_name_dto import UpdateNameDto
from dto.scrape_data.update_note_dto import UpdateNoteDto
from entities.scrape_data import ScrapeData
from handlers.pagination.pagination_handler import PaginationHandler
from handlers.pagination.response_pagination_handler import ResponsePaginationHandler
from repositories.scrape_data_repository import ScrapeDataRepository
from repositories.site_repository import SiteRepository
from services.interfaces.i_scrape_data_service import IScrapeDataService


class ScrapeDataService(IScrapeDataService):
    def __init__(self, db: Database):
        self._scrape_data_repository = ScrapeDataRepository(db)
        self._site_repository = SiteRepository(db)

    def get_by_account(self, account_guid: str, search: str, page: int, limit: int, order_by: int,
                       column_name: str, site_guid: str | None) -> ResponsePaginationHandler | None:
        try:
            result = self._scrape_data_repository.get_by_account(account_guid)

            result = [item for item in result if
                      (search.lower() in item.scrape_name.lower())]

            if column_name:
                if int(order_by) == 1:
                    result.sort(key=lambda x: getattr(x, column_name))
                elif int(order_by) == 2:
                    result.sort(key=lambda x: getattr(x, column_name), reverse=True)

            if site_guid:
                result = list(filter(lambda x: str(x.site_guid) == site_guid, result))

            if int(order_by) == 0:
                result.sort(key=lambda x: getattr(x, "created_date"), reverse=True)

            result = [GetScrapeDto(
                guid=data.guid,
                account_guid=data.account_guid,
                site_guid=data.site_guid,
                site_name=self._site_repository.get_by_guid(data.site_guid).site_name,
                scrape_name=data.scrape_name,
                data_count=data.data_count,
                favourite_count=data.favourite_count,
                web_data=data.web_data,
                scrape_time=data.scrape_time,
                created_date=data.created_date
            ) for data in result]

            return PaginationHandler.paginate(
                queryable=result,
                transform_function=lambda scrape_data, index: scrape_data.__dict__,
                page=page,
                limit=limit
            )
        except PyMongoError:
            return None

    def create_scrape_data(self, request: ScrapeDataRequestDto) -> ScrapeData | None:
        try:
            new_scrape_data = ScrapeData(
                str(uuid4()),
                request.account_guid,
                request.site_guid,
                request.scrape_name,
                request.data_count,
                0,
                request.web_data,
                request.scrape_time,
                datetime.utcnow() + timedelta(hours=7)
            )
            result = self._scrape_data_repository.create(new_scrape_data)
            if not result:
                return None
            return result
        except PyMongoError:
            return None

    def get_all_web_data(self, guid: str, search: str, page: int, limit: int, order_by: int,
                         column_name: str) -> ResponsePaginationHandler | None:
        try:
            result = self._scrape_data_repository.get_by_guid(guid).web_data

            if search:
                result = [web_data for web_data in result if
                          any(search.lower() in str(value).lower() for value in web_data.values())]

            if column_name:
                if int(order_by) == 1:
                    result.sort(key=lambda x: x[column_name])
                elif int(order_by) == 2:
                    result.sort(key=lambda x: x[column_name], reverse=True)

            return PaginationHandler.paginate(
                queryable=result,
                transform_function=lambda web_data, index: web_data,
                page=page,
                limit=limit
            )
        except PyMongoError:
            return None

    def get_fav_scrape_data(self, account_guid: str, search: str, page: int, limit: int, order_by: int,
                            column_name: str, site_guid: str | None) -> ResponsePaginationHandler | None:
        try:
            result = self._scrape_data_repository.get_by_account(account_guid)

            result = list(filter(lambda x: x.favourite_count > 0, result))

            result = [item for item in result if
                      (search.lower() in item.scrape_name.lower())]

            if column_name:
                if int(order_by) == 1:
                    result.sort(key=lambda x: getattr(x, column_name))
                elif int(order_by) == 2:
                    result.sort(key=lambda x: getattr(x, column_name), reverse=True)

            if site_guid:
                result = list(filter(lambda x: str(x.site_guid) == site_guid, result))

            if int(order_by) == 0:
                result.sort(key=lambda x: getattr(x, "created_date"), reverse=True)

            result = [GetScrapeDto(
                guid=data.guid,
                account_guid=data.account_guid,
                site_guid=data.site_guid,
                site_name=self._site_repository.get_by_guid(data.site_guid).site_name,
                scrape_name=data.scrape_name,
                data_count=data.data_count,
                favourite_count=data.favourite_count,
                web_data=data.web_data,
                scrape_time=data.scrape_time,
                created_date=data.created_date
            ) for data in result]

            return PaginationHandler.paginate(
                queryable=result,
                transform_function=lambda scrape_data, index: scrape_data.__dict__,
                page=page,
                limit=limit
            )
        except PyMongoError:
            return None

    def get_all_fav_web_data(self, guid: str, search: str, page: int, limit: int, order_by: int,
                             column_name: str) -> ResponsePaginationHandler | None:
        try:
            result = self._scrape_data_repository.get_by_guid(guid).web_data

            result = list(filter(lambda x: x["is_favourite"] == True, result))

            if search:
                result = [web_data for web_data in result if
                          any(search.lower() in str(value).lower() for value in web_data.values())]

            if column_name:
                if int(order_by) == 1:
                    result.sort(key=lambda x: x[column_name])
                elif int(order_by) == 2:
                    result.sort(key=lambda x: x[column_name], reverse=True)

            return PaginationHandler.paginate(
                queryable=result,
                transform_function=lambda web_data, index: web_data,
                page=page,
                limit=limit
            )
        except PyMongoError:
            return None

    def update_fav(self, request: UpdateFavDto) -> int:
        try:
            result = self._scrape_data_repository.update_favourite(request)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1

    def update_note(self, request: UpdateNoteDto) -> int:
        try:
            result = self._scrape_data_repository.update_note(request)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1

    def update_scrape(self, request: UpdateNameDto) -> bool:
        try:
            result = self._scrape_data_repository.update_name(request)
            return result
        except PyMongoError:
            return False

    def delete_scrape(self, guid: str) -> bool:
        try:
            result = self._scrape_data_repository.delete(guid)
            return result
        except PyMongoError:
            return False
