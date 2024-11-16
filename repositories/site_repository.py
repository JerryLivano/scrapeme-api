from pymongo.database import Database
from pymongo.errors import PyMongoError
from entities.site import Site
from repositories.interfaces.i_site_repository import ISiteRepository


class SiteRepository(ISiteRepository):
    def __init__(self, db: Database):
        self._collection = db['site']
        self._scrape_data_collection = db['scrape_data']

    def get_all(self) -> list[Site] | None:
        try:
            sites = self._collection.find()
            return [Site(
                site['guid'],
                site['admin_guid'],
                site['site_name'],
                site['site_url'],
                site['space_rule'],
                site['is_active'],
                site['url_pattern'],
                site['data_url_pattern'],
                site['created_date']
            ) for site in sites]
        except PyMongoError:
            return None

    def get_count(self) -> int:
        try:
            return self._collection.count_documents({})
        except PyMongoError:
            return 0

    def get_by_guid(self, guid: str) -> Site | None:
        try:
            site = self._collection.find_one({"guid": guid})
            if not site:
                return None
            return Site(
                site['guid'],
                site['admin_guid'],
                site['site_name'],
                site['site_url'],
                site['space_rule'],
                site['is_active'],
                site['url_pattern'],
                site['data_url_pattern'],
                site['created_date']
            )
        except PyMongoError:
            return None

    def create(self, site: Site) -> Site | None:
        try:
            result = self._collection.insert_one(site.to_dict())
            if not result:
                return None
            return site
        except PyMongoError:
            return None

    def update(self, site: Site) -> bool:
        try:
            result = self._collection.update_one(
                {"guid": site.guid},
                {"$set": site.to_dict()}
            )
            if not result:
                return False
            return True
        except PyMongoError:
            return False

    def update_active(self, guid: str, is_active: bool) -> bool:
        try:
            result = self._collection.update_one(
                {"guid": guid},
                {"$set": {"is_active": is_active}}
            )
            if not result:
                return False
            return True
        except PyMongoError:
            return False

    def delete(self, guid: str):
        try:
            result = self._collection.delete_one({"guid": guid})
            scrape_result = self._scrape_data_collection.delete_many({"site_guid": guid})
            if not result or not scrape_result:
                return False
            return result.deleted_count > 0
        except PyMongoError:
            return False
