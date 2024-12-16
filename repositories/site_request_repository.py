from pymongo.database import Database
from pymongo.errors import PyMongoError
from entities.site_request import SiteRequest
from repositories.interfaces.i_site_request_repository import ISiteRequestRepository

class SiteRequestRepository(ISiteRequestRepository):
    def __init__(self, db: Database):
        self._collection = db['site_request']

    def get_all(self) -> list[SiteRequest] | None:
        try:
            requests = self._collection.find()
            return [SiteRequest(
                request['guid'],
                request['account_guid'],
                request['subject'],
                request['site_url'],
                request['description'],
                request['status'],
                request['decline_reason'],
                request['created_date'],
                request['updated_date'],
            ) for request in requests]
        except PyMongoError:
            return None

    def get_count(self) -> int:
        try:
            return self._collection.count_documents({"status": 0})
        except PyMongoError:
            return 0

    def get_by_guid(self, guid: str) -> SiteRequest | None:
        try:
            request = self._collection.find_one({'guid': guid})
            if not request:
                return None
            return SiteRequest(
                request['guid'],
                request['account_guid'],
                request['subject'],
                request['site_url'],
                request['description'],
                request['status'],
                request['decline_reason'],
                request['created_date'],
                request['updated_date'],
            )
        except PyMongoError:
            return None

    def create(self, request: SiteRequest) -> SiteRequest | None:
        try:
            result = self._collection.insert_one(request.to_dict())
            if not result:
                return None
            return request
        except PyMongoError:
            return None

    def update(self, request: SiteRequest) -> bool:
        try:
            result = self._collection.update_one(
                {"guid": request.guid},
                {"$set": request.to_dict()}
            )
            if not result:
                return False
            return True
        except PyMongoError:
            return False

    def done_status(self, guid: str) -> bool:
        try:
            result = self._collection.update_one(
                {"guid": guid},
                {"$set": {"status": 2}}
            )
            if not result:
                return False
            return True
        except PyMongoError:
            return False

    def delete(self, guid: str) -> bool:
        try:
            result = self._collection.delete_one({"guid": guid})
            if not result:
                return False
            return result.deleted_count > 0
        except PyMongoError:
            return False

    def delete_many(self, account_guid: str) -> bool:
        try:
            result = self._collection.delete_many({"account_guid": account_guid})
            if not result:
                return False
            return result.deleted_count > 0
        except PyMongoError:
            return False
