from abc import ABC, abstractmethod
from dto.account.account_response_dto import AccountResponseDto
from dto.account.account_update_request_dto import AccountUpdateRequestDto
from dto.account.change_password_request_dto import ChangePasswordRequestDto
from dto.account.login_request_dto import LoginRequestDto
from dto.account.register_request_dto import RegisterRequestDto
from handlers.pagination.response_pagination_handler import ResponsePaginationHandler


class IAccountService(ABC):
    @abstractmethod
    def get_all(self, search: str, page: int, limit: int, is_active: int | None, role_name: str | None,
                order_by: int, column_name: str | None) -> ResponsePaginationHandler | None:
        pass

    @abstractmethod
    def get_by_guid(self, guid: str) -> AccountResponseDto | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> AccountResponseDto | None:
        pass

    @abstractmethod
    def update_account(self, update_request: AccountUpdateRequestDto) -> int:
        pass

    @abstractmethod
    def delete_account(self, guid: str) -> int:
        pass

    @abstractmethod
    def register(self, register_request: RegisterRequestDto) -> int:
        pass

    @abstractmethod
    def login(self, login_request: LoginRequestDto) -> int:
        pass

    @abstractmethod
    def change_password(self, request: ChangePasswordRequestDto) -> int:
        pass