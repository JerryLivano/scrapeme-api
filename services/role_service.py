from uuid import uuid4
from pymongo.errors import PyMongoError
from pymongo.database import Database
from dto.role.role_request_dto import RoleRequestDto
from dto.role.role_response_dto import RoleResponseDto
from entities.role import Role
from repositories.role_repository import RoleRepository
from services.account_service import AccountService
from services.interfaces.i_role_service import IRoleService

class RoleService(IRoleService):
    def __init__(self, db: Database):
        self._role_repository = RoleRepository(db)
        self._account_service = AccountService(db)

    def get_all(self) -> list[RoleResponseDto] | None:
        try:
            roles = self._role_repository.get_all()
            result = [
                RoleResponseDto(role.guid, role.role_name) for role in roles
            ]
            return result
        except PyMongoError:
            return None

    def get_by_guid(self, guid: str) -> RoleResponseDto | None:
        try:
            role = self._role_repository.get_by_guid(guid)
            if role:
                return RoleResponseDto(role.guid, role.role_name)
            return None
        except PyMongoError:
            return None

    def create_role(self, role: RoleRequestDto) -> RoleResponseDto | None:
        try:
            new_role: Role = Role(
                guid=str(uuid4()),
                role_name=role.role_name
            )
            result = self._role_repository.create(new_role)
            return RoleResponseDto(
                guid=result.guid,
                role_name=new_role.role_name
            )
        except PyMongoError:
            return None

    def update_role(self, guid: str, updated_role: RoleRequestDto) -> int:
        try:
            role = self._role_repository.get_by_guid(guid)
            if not role:
                return -2
            new_role = Role(role.guid, updated_role.role_name)
            result = self._role_repository.update(new_role)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1

    def delete_role(self, guid: str) -> int:
        try:
            role = self._role_repository.get_by_guid(guid)
            if not role:
                return 0

            result = self._role_repository.delete(guid)
            if result:
                return 1
        except PyMongoError:
            return -1
