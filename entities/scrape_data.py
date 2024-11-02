from datetime import time, datetime


class ScrapeData:
    def __init__(self, guid: str, account_guid: str, site_guid: str, scrape_name: str, limit_data: int, data_count: int,
                 favourite_count: int, web_data: list[dict], scrape_time: time, created_date: datetime):
        self.guid = guid
        self.account_guid = account_guid
        self.site_guid = site_guid
        self.scrape_name = scrape_name
        self.limit_data = limit_data
        self.data_count = data_count
        self.favourite_count = favourite_count
        self.web_data = web_data
        self.scrape_time = scrape_time
        self.created_date = created_date

    def to_dict(self):
        return {
            'guid': self.guid,
            'account_guid': self.account_guid,
            'site_guid': self.site_guid,
            'scrape_name': self.scrape_name,
            'limit_data': self.limit_data,
            'data_count': self.data_count,
            'favourite_count': self.favourite_count,
            'web_data': self.web_data,
            'scrape_time': self.scrape_time,
            'created_date': self.created_date
        }
