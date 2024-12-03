from pymongo.database import Database
from pymongo.errors import PyMongoError
from entities.template import Template
from repositories.interfaces.i_template_repository import ITemplateRepository


class TemplateRepository(ITemplateRepository):
    def __init__(self, db: Database):
        self._collection = db['template']

    def get_all(self) -> list[Template] | None:
        try:
            templates = self._collection.find()
            return [Template(
                template['guid'],
                template['container'],
                template['container_tag'],
                template['is_class'],
                template['is_id'],
                template['site_guid'],
                template['tag_data']
            ) for template in templates]
        except PyMongoError:
            return None

    def get_by_guid(self, guid: str) -> Template | None:
        try:
            template = self._collection.find_one({"guid": guid})
            if not template:
                return None
            return Template(
                template['guid'],
                template['container'],
                template['container_tag'],
                template['is_class'],
                template['is_id'],
                template['site_guid'],
                template['tag_data']
            )
        except PyMongoError:
            return None

    def get_by_site_guid(self, site_guid: str) -> Template | None:
        try:
            template = self._collection.find_one({"site_guid": site_guid})
            if not template:
                return None
            return Template(
                template['guid'],
                template['container'],
                template['container_tag'],
                template['is_class'],
                template['is_id'],
                template['site_guid'],
                template['tag_data']
            )
        except PyMongoError:
            return None

    def create(self, template: Template) -> Template | None:
        try:
            result = self._collection.insert_one(template.to_dict())
            if not result:
                return None
            return template
        except PyMongoError:
            return None

    def update(self, template: Template) -> bool:
        try:
            result = self._collection.update_one(
                {"guid": template.guid},
                {"$set": template.to_dict()}
            )
            if not result:
                return False
            return True
        except PyMongoError:
            return False

    def delete(self, guid: str):
        try:
            result = self._collection.delete_one({"guid": guid})
            if not result:
                return False
            return result.deleted_count > 0
        except PyMongoError:
            return False
