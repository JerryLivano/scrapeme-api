from abc import ABC, abstractmethod
from dto.category.category_add_request_dto import CategoryAddRequestDto
from entities.category import Category
from handlers.pagination.response_pagination_handler import ResponsePaginationHandler


class ICategoryService(ABC):
    @abstractmethod
    def get_all(self, search: str, page: int, limit: int, order_by: int,
                column_name: str) -> ResponsePaginationHandler | None:
        pass

    @abstractmethod
    def get_by_guid(self, guid: str) -> Category | None:
        pass

    @abstractmethod
    def create_category(self, category: Category) -> Category | None:
        pass

    @abstractmethod
    def update_category(self, category_request: CategoryAddRequestDto) -> int:
        pass

    @abstractmethod
    def delete_category(self, guid: str) -> int:
        pass
