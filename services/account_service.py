from datetime import datetime, timedelta
from uuid import uuid4
from pymongo.database import Database
from pymongo.errors import PyMongoError
from dto.account.account_response_dto import AccountResponseDto
from dto.account.account_update_request_dto import AccountUpdateRequestDto
from dto.account.change_password_request_dto import ChangePasswordRequestDto
from dto.account.login_request_dto import LoginRequestDto
from dto.account.register_request_dto import RegisterRequestDto
from entities.account import Account
from entities.user import User
from handlers.bcrypt_handler import BCryptHandler
from handlers.pagination.pagination_handler import PaginationHandler
from handlers.pagination.response_pagination_handler import ResponsePaginationHandler
from repositories.account_repository import AccountRepository
from repositories.role_repository import RoleRepository
from repositories.site_request_repository import SiteRequestRepository
from repositories.user_repository import UserRepository
from services.interfaces.i_account_service import IAccountService


class AccountService(IAccountService):
    def __init__(self, db: Database):
        self._account_repository = AccountRepository(db)
        self._user_repository = UserRepository(db)
        self._role_repository = RoleRepository(db)
        self._request_repository = SiteRequestRepository(db)
        self._bcrypt = BCryptHandler()

    def get_all(self, search: str, page: int, limit: int, active_status: int | None, role_name: str | None,
                order_by: int, column_name: str | None) -> ResponsePaginationHandler | None:
        try:
            accounts = self._account_repository.get_all()

            result = [
                AccountResponseDto(
                    account=account,
                    user=self._user_repository.get_by_guid(account.user_guid),
                    role=self._role_repository.get_by_guid(account.role_guid)
                ) for account in accounts
            ]

            result = [
                data for data in result
                if (search.lower() in (
                    data.user['first_name'] + ((" " + data.user['last_name']) if data.user['last_name'] else "")).lower())
                   or (search.lower() in data.user['email'].lower())
            ]

            if int(active_status) == 1:
                result = list(filter(lambda x: x.is_active, result))
            elif int(active_status) == 0:
                result = list(filter(lambda x: x.is_active == False, result))

            if role_name:
                result = list(filter(lambda x: x.role['role_name'].lower() == role_name.lower(), result))

            if column_name:
                if int(order_by) == 1:
                    result.sort(key=lambda x: x.user[column_name])
                elif int(order_by) == 2:
                    result.sort(key=lambda x: x.user[column_name], reverse=True)

            if int(order_by) == 0:
                result.sort(key=lambda x: getattr(x, "created_date"), reverse=True)

            return PaginationHandler.paginate(
                queryable=result,
                transform_function=lambda account, index: account.__dict__,
                page=page,
                limit=limit
            )
        except PyMongoError:
            return None

    def get_by_guid(self, guid: str) -> AccountResponseDto | None:
        try:
            account = self._account_repository.get_by_guid(guid)
            return AccountResponseDto(
                account=account,
                user=self._user_repository.get_by_guid(account.user_guid),
                role=self._role_repository.get_by_guid(account.role_guid)
            )
        except PyMongoError:
            return None

    def get_by_email(self, email: str) -> AccountResponseDto | None:
        try:
            user = self._user_repository.get_by_email(email)
            account = self._account_repository.get_by_user_guid(user.guid)
            return AccountResponseDto(
                account=account,
                user=user,
                role=self._role_repository.get_by_guid(account.role_guid)
            )
        except PyMongoError:
            return None

    def update_account(self, update_request: AccountUpdateRequestDto) -> int:
        try:
            account = self._account_repository.get_by_guid(update_request.guid)
            user = self._user_repository.get_by_guid(account.user_guid)
            role = self._role_repository.get_by_guid(update_request.role_guid)
            if not account or not user:
                return -2

            email_exist = self._user_repository.get_by_email(update_request.email[0])
            if email_exist and (email_exist.guid != user.guid):
                return -3

            new_user = User(
                guid=user.guid,
                first_name=update_request.first_name[0],
                last_name=update_request.last_name[0],
                email=update_request.email[0]
            )

            new_account = Account(
                guid=update_request.guid,
                user_guid=new_user.guid,
                role_guid=role.guid,
                password=account.password,
                is_active=update_request.is_active[0],
                created_by=account.created_by,
                created_date=account.created_date
            )

            result_account = self._account_repository.update(new_account)
            result_user = self._user_repository.update(new_user)
            if not result_user or not result_account:
                return 0
            return 1
        except PyMongoError:
            return -1

    def delete_account(self, guid: str) -> int:
        try:
            account = self._account_repository.get_by_guid(guid)
            if not account:
                return -2

            delete_user = self._user_repository.delete(account.user_guid)
            delete_account = self._account_repository.delete(guid)
            delete_request = self._request_repository.delete_many(guid)

            if not delete_user or not delete_account or not delete_request:
                return 0

            return 1
        except PyMongoError:
            return -1

    def register(self, register_request: RegisterRequestDto) -> int:
        try:
            if register_request.password != register_request.confirm_password:
                return -2

            user_exist = self._user_repository.get_by_email(register_request.email)

            if user_exist:
                return -3

            new_user: User = User(
                guid=str(uuid4()),
                first_name=register_request.first_name,
                last_name=register_request.last_name,
                email=register_request.email
            )

            role = self._role_repository.get_by_guid(register_request.role_guid)

            new_account: Account = Account(
                guid=str(uuid4()),
                user_guid=new_user.guid,
                role_guid=role.guid,
                password=self._bcrypt.hash_password(register_request.password),
                is_active=True,
                created_by=register_request.created_by if register_request.created_by else "root",
                created_date=datetime.utcnow() + timedelta(hours=7)
            )

            user_result = self._user_repository.create(new_user)
            account_result = self._account_repository.create(new_account)

            if not user_result or not account_result:
                return 0

            return 1
        except PyMongoError:
            return -1

    def login(self, login_request: LoginRequestDto) -> int:
        try:
            user = self._user_repository.get_by_email(login_request.email)
            if not user:
                return 0

            account = self._account_repository.get_by_user_guid(user.guid)
            if not account or not self._bcrypt.verify_password(login_request.password, account.password):
                return 0

            if not account.role_guid:
                return -3

            if not account.is_active:
                return -2

            return 1
        except PyMongoError:
            return -1

    def change_password(self, request: ChangePasswordRequestDto) -> int:
        try:
            if request.password != request.confirm_password:
                return -3  # Password not match

            account = self._account_repository.get_by_guid(request.guid)
            if not account:
                return -2  # Account not found

            hashed_password = self._bcrypt.hash_password(request.password)
            if not hashed_password:
                return 0

            result = self._account_repository.update_password(request.guid, hashed_password)
            if not result:
                return 0

            return 1
        except PyMongoError:
            return -1
