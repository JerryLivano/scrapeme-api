from abc import ABC, abstractmethod
from entities.template import Template


class ITemplateRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Template] | None:
        pass

    @abstractmethod
    def get_by_guid(self, guid: str) -> Template | None:
        pass

    @abstractmethod
    def get_by_site_guid(self, site_guid: str) -> Template | None:
        pass

    @abstractmethod
    def create(self, template: Template) -> Template | None:
        pass

    @abstractmethod
    def update(self, template: Template) -> bool:
        pass

    @abstractmethod
    def delete(self, guid: str):
        pass