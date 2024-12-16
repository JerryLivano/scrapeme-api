from abc import ABC, abstractmethod
from dto.template.template_request_dto import TemplateRequestDto
from dto.template.template_update_request_dto import TemplateUpdateRequestDto
from entities.template import Template


class ITemplateService(ABC):
    @abstractmethod
    def get_by_site_guid(self, site_guid: str) -> Template | None:
        pass

    @abstractmethod
    def create_template(self, request: TemplateRequestDto) -> Template | None:
        pass

    @abstractmethod
    def update_template(self, request: TemplateUpdateRequestDto) -> int:
        pass

    @abstractmethod
    def delete_template(self, guid: str) -> int:
        pass