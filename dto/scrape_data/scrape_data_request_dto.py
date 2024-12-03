class ScrapeDataRequestDto:
    def __init__(self, account_guid: str, site_guid: str, scrape_name: str, data_count: int,
                 web_data: list[dict], scrape_time: str):
        self.account_guid = account_guid
        self.site_guid = site_guid
        self.scrape_name = scrape_name
        self.data_count = data_count
        self.web_data = web_data
        self.scrape_time = scrape_time
