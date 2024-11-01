from pymongo.errors import PyMongoError
from pymongo.database import Database
from entities.role import Role
from repositories.interfaces.i_role_repository import IRoleRepository

class RoleRepository(IRoleRepository):
    def __init__(self, db: Database):
        self._collection = db['role']
        self._account_collection = db['account']

    def get_all(self) -> list[Role] | None:
        try:
            roles = self._collection.find()
            return [Role(role['guid'], role['role_name']) for role in roles]
        except PyMongoError:
            return None

    def get_by_guid(self, guid: str) -> Role | None:
        try:
            role = self._collection.find_one({"guid": guid})
            if role:
                return Role(role['guid'], role['role_name'])
            return None
        except PyMongoError:
            return None

    def create(self, role: Role) -> Role | None:
        try:
            self._collection.insert_one(role.to_dict())
            return role
        except PyMongoError:
            return None

    def update(self, role: Role) -> bool:
        try:
            result = self._collection.update_one(
                {"guid": role.guid},
                {"$set": role.to_dict()}
            )
            if not result:
                return False
            return result.modified_count > 0
        except PyMongoError:
            return False

    def delete(self, guid: str) -> bool:
        try:
            result = self._collection.delete_one({"guid": guid})
            account_result = self._account_collection.update_many(
                {"role_guid": guid},
                {"$set": {"role_guid": None}}
            )
            if not result or not account_result:
                return False
            return result.deleted_count > 0
        except PyMongoError:
            return False


