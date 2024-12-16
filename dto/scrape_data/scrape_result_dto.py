from datetime import datetime


class ScrapeResultDto:
    def __init__(self, response: int, scrape_guid: str, scrape_name: str, created_date: datetime):
        self.response = response
        self.scrape_guid = scrape_guid
        self.scrape_name = scrape_name
        self.created_date = created_date