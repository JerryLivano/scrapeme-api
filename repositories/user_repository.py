from pymongo.database import Database
from pymongo.errors import PyMongoError
from entities.user import User
from repositories.interfaces.i_user_repository import IUserRepository

class UserRepository(IUserRepository):
    def __init__(self, db: Database):
        self._collection = db['user']

    def get_all(self) -> list[User] | None:
        try:
            users = self._collection.find()
            if not users:
                return None
            return [User(
                guid=user['guid'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                email=user['email']
            ) for user in users]
        except PyMongoError:
            return None

    def get_by_guid(self, guid: str) -> User | None:
        try:
            user = self._collection.find_one({"guid": guid})
            if not user:
                return None
            return User(
                guid=user['guid'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                email=user['email']
            )
        except PyMongoError:
            return None

    def create(self, user: User) -> User | None:
        try:
            result = self._collection.insert_one(user.to_dict())
            if not result:
                return None
            return user
        except PyMongoError:
            return None

    def update(self, user: User) -> User | None:
        try:
            result = self._collection.update_one(
                {"guid": user.guid},
                {"$set": user.to_dict()}
            )
            if not result:
                return None
            return user
        except PyMongoError:
            return None

    def delete(self, guid: str) -> bool:
        try:
            result = self._collection.delete_one({"guid": guid})
            return result.deleted_count > 0
        except PyMongoError:
            return False

    def get_by_email(self, email: str) -> User | None:
        try:
            user = self._collection.find_one({"email": email})
            if not user:
                return None
            return User(
                user["guid"],
                user["first_name"],
                user["last_name"],
                user["email"]
            )
        except PyMongoError:
            return None
