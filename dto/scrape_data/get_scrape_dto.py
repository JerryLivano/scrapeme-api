from datetime import datetime


class GetScrapeDto:
    def __init__(self, guid: str, account_guid: str, site_guid: str, site_name: str, scrape_name: str, data_count: int,
                 favourite_count: int, web_data: list[dict], scrape_time: str, created_date: datetime):
        self.guid = guid
        self.account_guid = account_guid
        self.site_guid = site_guid
        self.site_name = site_name
        self.scrape_name = scrape_name
        self.data_count = data_count
        self.favourite_count = favourite_count
        self.web_data = web_data
        self.scrape_time = scrape_time
        self.created_date = created_date