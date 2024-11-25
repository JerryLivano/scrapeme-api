from datetime import datetime, timedelta
from uuid import uuid4
from pymongo.database import Database
from pymongo.errors import PyMongoError
from dto.site.create_url_dto import CreateUrlDto
from dto.site.site_active_update_dto import SiteUpdateActiveDto
from dto.site.site_request_dto import SiteRequestDto
from dto.site.site_update_request_dto import SiteUpdateRequestDto
from entities.site import Site
from handlers.pagination.pagination_handler import PaginationHandler
from handlers.pagination.response_pagination_handler import ResponsePaginationHandler
from repositories.category_repository import CategoryRepository
from repositories.site_repository import SiteRepository
from repositories.template_repository import TemplateRepository
from services.interfaces.i_site_service import ISiteService


class SiteService(ISiteService):
    def __init__(self, db: Database):
        self._site_repository = SiteRepository(db)
        self._category_repository = CategoryRepository(db)
        self._template_repository = TemplateRepository(db)

    def create_url(self, site_guid: str) -> CreateUrlDto | None:
        try:
            site = self._site_repository.get_by_guid(site_guid)
            if not site:
                return None

            result = CreateUrlDto(
                (site.site_url + ("".join([
                    f"{str(item['identifier'])}{f"{str(item.get('form_id')).replace(" ", site.space_rule)}" if item.get('form_id') else ""}"
                    for item in site.url_pattern]))) if site.url_pattern else None,
                (site.site_url + ("".join([
                    f"{str(item['identifier'])}{f"{str(item.get('form_id')).replace(" ", site.space_rule)}" if item.get('form_id') else ""}"
                    for item in site.data_url_pattern]))) if site.data_url_pattern else None,
            )
            return result
        except ValueError:
            return None

    def get_all(self, search: str, page: int, limit: int, order_by: int,
                column_name: str, status: bool | None) -> ResponsePaginationHandler | None:
        try:
            sites = self._site_repository.get_all()

            sites = [data for data in sites if search.lower() in data.site_name.lower()]

            if status is not None:
                if status == "true":
                    sites = list(filter(lambda x: x.is_active == True, sites))
                else:
                    sites = list(filter(lambda x: x.is_active == False, sites))

            if column_name:
                if int(order_by) == 1:
                    sites.sort(key=lambda x: getattr(x, column_name))
                elif int(order_by) == 2:
                    sites.sort(key=lambda x: getattr(x, column_name), reverse=True)

            if int(order_by) == 0:
                sites.sort(key=lambda x: getattr(x, "created_date"), reverse=True)

            return PaginationHandler.paginate(
                queryable=sites,
                transform_function=lambda site, index: site.__dict__,
                page=page,
                limit=limit
            )
        except PyMongoError:
            return None

    def create_site(self, request: SiteRequestDto) -> Site | None:
        try:
            new_site: Site = Site(
                guid=str(uuid4()),
                admin_guid=request.admin_guid,
                site_name=request.site_name,
                site_url=request.site_url,
                space_rule=request.space_rule,
                is_active=False,
                url_pattern=request.url_pattern,
                data_url_pattern=request.data_url_pattern,
                created_date=datetime.utcnow() + timedelta(hours=7)
            )
            print(new_site.created_date)
            result = self._site_repository.create(new_site)
            if not result:
                return None
            return result
        except PyMongoError:
            return None

    def update_site(self, request: SiteUpdateRequestDto) -> int:
        try:
            site = self._site_repository.get_by_guid(request.guid)
            if not site:
                return -2
            new_site = Site(
                request.guid,
                site.admin_guid,
                request.site_name,
                request.site_url,
                request.space_rule,
                site.is_active,
                request.url_pattern,
                request.data_url_pattern,
                site.created_date
            )
            result = self._site_repository.update(new_site)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1

    def update_active_site(self, request: SiteUpdateActiveDto) -> int:
        try:
            site = self._site_repository.get_by_guid(request.guid)
            if not site:
                return -2
            result = self._site_repository.update_active(request.guid, request.is_active)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1

    def delete_site(self, guid: str) -> int:
        try:
            # template = self._template_repository.get_by_site_guid(guid)
            # if not template:
            #     return -2

            # delete_template = self._template_repository.delete(guid)
            delete_site = self._site_repository.delete(guid)

            if not delete_site:
                return 0
            return 1
        except PyMongoError:
            return -1
