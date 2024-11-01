from pymongo.database import Database
from pymongo.errors import PyMongoError
from entities.category import Category
from repositories.interfaces.i_category_repository import ICategoryRepository

class CategoryRepository(ICategoryRepository):
    def __init__(self, db: Database):
        self._collection = db['category']
        self._site_collection = db['site']

    def get_all(self) -> list[Category] | None:
        try:
            categories = self._collection.find()
            return [Category(category['guid'], category['category_name']) for category in categories]
        except PyMongoError:
            return None

    def get_by_guid(self, guid: str) -> Category | None:
        try:
            category = self._collection.find_one({"guid": guid})
            if category:
                return Category(category['guid'], category['category_name'])
            return None
        except PyMongoError:
            return None

    def create(self, category: Category) -> Category | None:
        try:
            result = self._collection.insert_one(category.to_dict())
            if not result:
                return None
            return category
        except PyMongoError:
            return None

    def update(self, category: Category) -> bool:
        try:
            result = self._collection.update_one(
                {"guid": category.guid},
                {"$set": category.to_dict()}
            )
            if not result:
                return False
            return True
        except PyMongoError:
            return False

    def delete(self, guid: str) -> bool:
        try:
            result = self._collection.delete_one({"guid": guid})
            scrape_result = self._site_collection.update_many(
                {"category_guid": guid},
                {"$set": {"category_guid": None}}
            )
            if not result or not scrape_result:
                return False
            return result.deleted_count > 0
        except PyMongoError:
            return False