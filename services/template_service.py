from uuid import uuid4
from pymongo.database import Database
from pymongo.errors import PyMongoError
from dto.template.template_request_dto import TemplateRequestDto
from dto.template.template_update_request_dto import TemplateUpdateRequestDto
from entities.template import Template
from repositories.template_repository import TemplateRepository
from services.interfaces.i_template_service import ITemplateService


class TemplateService(ITemplateService):
    def __init__(self, db: Database):
        self._template_repository = TemplateRepository(db)

    def get_by_site_guid(self, site_guid: str) -> Template | None:
        try:
            template = self._template_repository.get_by_site_guid(site_guid)
            if not template:
                return None
            return template
        except PyMongoError:
            return None

    def create_template(self, request: TemplateRequestDto) -> Template | None:
        try:
            new_template = Template(
                guid=str(uuid4()),
                site_guid=request.site_guid,
                container=request.container,
                container_tag=request.container_tag,
                is_class=request.is_class,
                is_id=request.is_id,
                tag_data=request.tag_data
            )
            result = self._template_repository.create(new_template)
            if not result:
                return None
            return result
        except PyMongoError:
            return None

    def update_template(self, request: TemplateUpdateRequestDto) -> int:
        try:
            template = self._template_repository.get_by_guid(request.guid)
            if not template:
                return -2
            new_template = Template(
                guid=request.guid,
                site_guid=template.site_guid,
                container=request.container,
                container_tag=request.container_tag,
                is_class=request.is_class,
                is_id=request.is_id,
                tag_data=request.tag_data
            )
            result = self._template_repository.update(new_template)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1

    def delete_template(self, guid: str) -> int:
        try:
            result = self._template_repository.delete(guid)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1
