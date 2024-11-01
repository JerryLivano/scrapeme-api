from uuid import uuid4
from pymongo.database import Database
from pymongo.errors import PyMongoError
from dto.category.category_add_request_dto import CategoryAddRequestDto
from dto.category.category_update_request_dto import CategoryUpdateRequestDto
from entities.category import Category
from handlers.pagination.pagination_handler import PaginationHandler
from handlers.pagination.response_pagination_handler import ResponsePaginationHandler
from repositories.category_repository import CategoryRepository
from services.interfaces.i_category_service import ICategoryService

class CategoryService(ICategoryService):
    def __init__(self, db: Database):
        self._category_repository = CategoryRepository(db)

    def get_all(self, search: str, page: int, limit: int, order_by: int, column_name: str) -> ResponsePaginationHandler | None:
        try:
            categories = self._category_repository.get_all()

            categories = [category for category in categories if search.lower() in category.category_name.lower()]

            if order_by != 0 and column_name:
                if int(order_by) == 1:
                    categories.sort(key=lambda x: getattr(x, column_name))
                elif int(order_by) == 2:
                    categories.sort(key=lambda x: getattr(x, column_name), reverse=True)

            return PaginationHandler.paginate(
                queryable=categories,
                transform_function=lambda category, index: category.__dict__,
                page=page,
                limit=limit
            )
        except PyMongoError:
            return None

    def get_by_guid(self, guid: str) -> Category | None:
        try:
            category = self._category_repository.get_by_guid(guid)
            if not category:
                return None
            return category
        except PyMongoError:
            return None

    def create_category(self, category: CategoryAddRequestDto) -> Category | None:
        try:
            new_category = Category(
                str(uuid4()),
                category.category_name
            )
            result = self._category_repository.create(new_category)
            if not result:
                return None
            return result
        except PyMongoError:
            return None

    def update_category(self, updated_category: CategoryUpdateRequestDto) -> int:
        try:
            category = self._category_repository.get_by_guid(updated_category.guid)
            if not category:
                return -2
            new_category = Category(updated_category.guid, updated_category.category_name)
            result = self._category_repository.update(new_category)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1

    def delete_category(self, guid: str) -> int:
        try:
            result = self._category_repository.delete(guid)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1