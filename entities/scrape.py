from datetime import datetime

class Scrape:
    def __init__(self, guid: str, site_guid: str, account_guid: str, category_guid: str, scrape_name: str, description: str,
                 html_tag: list[dict], created_date: datetime):
        self.guid = guid
        self.site_guid = site_guid
        self.account_guid = account_guid
        self.category_guid = category_guid
        self.scrape_name = scrape_name
        self.description = description
        self.html_tag = html_tag
        self.created_date = created_date

    def to_dict(self):
        return {
            'guid': self.guid,
            'site_guid': self.site_guid,
            'account_guid': self.account_guid,
            'category_guid': self.category_guid,
            'scrape_name': self.scrape_name,
            'description': self.description,
            'html_tag': self.html_tag,
            'created_date': self.created_date
        }