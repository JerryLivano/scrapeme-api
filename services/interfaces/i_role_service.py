from abc import ABC, abstractmethod
from dto.role.role_request_dto import RoleRequestDto
from dto.role.role_response_dto import RoleResponseDto

class IRoleService(ABC):
    @abstractmethod
    def get_all(self) -> list[RoleResponseDto] | None:
        pass

    @abstractmethod
    def get_by_guid(self, guid: str) -> RoleResponseDto | None:
        pass

    @abstractmethod
    def create_role(self, role: RoleRequestDto) -> RoleResponseDto | None:
        pass

    @abstractmethod
    def update_role(self, guid: str, updated_role: RoleRequestDto) -> int:
        pass

    @abstractmethod
    def delete_role(self, guid: str) -> int:
        pass
