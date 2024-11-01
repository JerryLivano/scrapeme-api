from datetime import datetime, timedelta
from uuid import uuid4
from pymongo.database import Database
from pymongo.errors import PyMongoError
from dto.site_request.site_request_decline_dto import SiteRequestDeclineDto
from dto.site_request.site_request_request_dto import SiteRequestRequestDto
from dto.site_request.site_request_update_request_dto import SiteRequestUpdateRequestDto
from entities.site_request import SiteRequest
from handlers.pagination.pagination_handler import PaginationHandler
from handlers.pagination.response_pagination_handler import ResponsePaginationHandler
from repositories.site_request_repository import SiteRequestRepository
from services.interfaces.i_site_request_service import ISiteRequestService

class SiteRequestService(ISiteRequestService):
    def __init__(self, db: Database):
        self._request_repository = SiteRequestRepository(db)

    def get_all(self, search: str, page: int, limit: int, order_by: int,
                column_name: str) -> ResponsePaginationHandler | None:
        try:
            requests = self._request_repository.get_all()

            requests = [request for request in requests if
                        ((search.lower() in request.subject.lower()) or (search.lower() in request.site_name.lower()))]

            if order_by != 0 and column_name:
                if int(order_by) == 1:
                    requests.sort(key=lambda x: getattr(x, column_name))
                elif int(order_by) == 2:
                    requests.sort(key=lambda x: getattr(x, column_name), reverse=True)

            return PaginationHandler.paginate(
                queryable=requests,
                transform_function=lambda request, index: request.__dict__,
                page=page,
                limit=limit
            )
        except PyMongoError:
            return None

    def get_by_account(self, account: str, search: str, page: int, limit: int, order_by: int,
                       column_name: str) -> ResponsePaginationHandler | None:
        try:
            requests = self._request_repository.get_all()

            requests = list(filter(lambda x: x.account_guid == account, requests))

            requests = [request for request in requests if
                        ((search.lower() in request.subject.lower()) or (search.lower() in request.site_name.lower()))]

            if order_by != 0 and column_name:
                if int(order_by) == 1:
                    requests.sort(key=lambda x: getattr(x, column_name))
                elif int(order_by) == 2:
                    requests.sort(key=lambda x: getattr(x, column_name), reverse=True)

            return PaginationHandler.paginate(
                queryable=requests,
                transform_function=lambda request, index: request.__dict__,
                page=page,
                limit=limit
            )
        except PyMongoError:
            return None

    def get_by_guid(self, guid: str) -> SiteRequest | None:
        try:
            category = self._request_repository.get_by_guid(guid)
            if not category:
                return None
            return category
        except PyMongoError:
            return None

    def create_request(self, request: SiteRequestRequestDto) -> SiteRequest | None:
        try:
            new_request = SiteRequest(
                str(uuid4()),
                request.account_guid,
                request.subject,
                request.site_url,
                request.description,
                None,
                None,
                datetime.utcnow() + timedelta(hours=7),
                None
            )
            result = self._request_repository.create(new_request)
            if not result:
                return None
            return result
        except PyMongoError:
            return None

    def update_request(self, update_request: SiteRequestUpdateRequestDto) -> int:
        try:
            request = self._request_repository.get_by_guid(update_request.guid)
            if not request:
                return -2
            new_request = SiteRequest(
                update_request.guid,
                request.account_guid,
                update_request.subject,
                update_request.site_url,
                update_request.description,
                request.status,
                request.decline_reason,
                request.created_date,
                request.updated_date
            )
            result = self._request_repository.update(new_request)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1

    def accept(self, guid: str) -> int:
        try:
            request = self._request_repository.get_by_guid(guid)
            if not request:
                return -2
            new_request = SiteRequest(
                guid,
                request.account_guid,
                request.subject,
                request.site_url,
                request.description,
                True,
                request.decline_reason,
                request.created_date,
                datetime.utcnow() + timedelta(hours=7)
            )
            result = self._request_repository.update(new_request)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1

    def decline(self, decline_request: SiteRequestDeclineDto) -> int:
        try:
            request = self._request_repository.get_by_guid(decline_request.guid)
            if not request:
                return -2
            new_request = SiteRequest(
                decline_request.guid,
                request.account_guid,
                request.subject,
                request.site_url,
                request.description,
                False,
                decline_request.decline_reason,
                request.created_date,
                datetime.utcnow() + timedelta(hours=7)
            )
            result = self._request_repository.update(new_request)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1

    def delete_request(self, guid: str) -> int:
        try:
            result = self._request_repository.delete(guid)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1
