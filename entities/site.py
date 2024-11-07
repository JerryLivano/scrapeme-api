from datetime import datetime


class Site:
    def __init__(self, guid: str, admin_guid: str, site_name: str, site_url: str,
                 space_rule: str | None, is_active: bool, url_pattern: list[dict], data_url_pattern: list[dict] | None,
                 created_date: datetime):
        self.guid = guid
        self.admin_guid = admin_guid
        self.site_name = site_name
        self.site_url = site_url
        self.space_rule = space_rule
        self.is_active = is_active
        self.url_pattern = url_pattern
        self.data_url_pattern = data_url_pattern
        self.created_date = created_date

    def to_dict(self):
        return {
            'guid': self.guid,
            'admin_guid': self.admin_guid,
            'site_name': self.site_name,
            'site_url': self.site_url,
            'space_rule': self.space_rule,
            'is_active': self.is_active,
            'url_pattern': self.url_pattern,
            'data_url_pattern': self.data_url_pattern,
            'created_date': self.created_date
        }
