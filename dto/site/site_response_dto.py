from datetime import datetime
from entities.category import Category

class SiteResponseDto:
    def __init__(self, guid: str, admin_guid: str, categories: list[Category], site_name: str, site_url: str,
                 url_pattern: str, data_url_pattern: str | None, created_date: datetime):
        self.guid = guid
        self.admin_guid = admin_guid
        self.categories = [category.to_dict() for category in categories]
        self.site_name = site_name
        self.site_url = site_url
        self.url_pattern = url_pattern
        self.data_url_pattern = data_url_pattern
        self.created_date = created_date
