from pymongo.database import Database
from pymongo.errors import PyMongoError
from entities.account import Account
from repositories.interfaces.i_account_repository import IAccountRepository

class AccountRepository(IAccountRepository):
    def __init__(self, db: Database):
        self._collection = db['account']
        self._request_collection = db['site_request']

    def get_all(self) -> list[Account] | None:
        try:
            accounts = self._collection.find()
            if not accounts:
                return None
            return [Account(
                guid=account['guid'],
                user_guid=account['user_guid'],
                role_guid=account.get("role_guid", None),
                password=account['password'].decode('utf-8') if isinstance(account['password'], bytes) else account[
                    'password'],
                is_active=account['is_active'],
                created_by=account['created_by'],
                created_date=account['created_date']
            ) for account in accounts]
        except PyMongoError:
            return None

    def get_count(self) -> int:
        try:
            return self._collection.count_documents({})
        except PyMongoError:
            return 0

    def get_by_guid(self, guid: str) -> Account | None:
        try:
            result = self._collection.find_one({"guid": guid})
            if result:
                return Account(
                    guid=result['guid'],
                    user_guid=result['user_guid'],
                    role_guid=result['role_guid'] if result['role_guid'] else None,
                    password=result['password'].decode('utf-8') if isinstance(result['password'], bytes) else result[
                        'password'],
                    is_active=result['is_active'],
                    created_by=result['created_by'],
                    created_date=result['created_date']
                )
            return None
        except PyMongoError:
            return None

    def create(self, account: Account) -> Account | None:
        try:
            result = self._collection.insert_one(account.to_dict())
            if not result:
                return None
            return account
        except PyMongoError:
            return None

    def update(self, account: Account) -> Account | None:
        try:
            result = self._collection.update_one(
                {"guid": account.guid},
                {"$set": account.to_dict()}
            )
            if not result:
                return None
            return account
        except PyMongoError:
            return None

    def update_password(self, guid: str, changed_password: bytes) -> bool:
        try:
            result = self._collection.update_one(
                {"guid": guid},
                {"$set": {"password": changed_password}}
            )
            if not result:
                return False
            return True
        except PyMongoError:
            return False

    def delete(self, guid: str) -> bool:
        try:
            result = self._collection.delete_one({"guid": guid})
            request_result = self._request_collection.delete_many({'account_guid': guid})
            if not result or not request_result:
                return False
            return result.deleted_count > 0
        except PyMongoError:
            return False

    def get_by_user_guid(self, guid: str) -> Account | None:
        try:
            result = self._collection.find_one({"user_guid": guid})
            if result:
                return Account(
                    guid=result['guid'],
                    user_guid=result['user_guid'],
                    role_guid=result['role_guid'] if result['role_guid'] else None,
                    password=result['password'].decode('utf-8') if isinstance(result['password'], bytes) else result[
                        'password'],
                    is_active=result['is_active'],
                    created_by=result['created_by'],
                    created_date=result['created_date']
                )
            return None
        except PyMongoError:
            return None
