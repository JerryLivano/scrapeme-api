class ScrapeDataDto:
    def __init__(self, site_guid: str, account_guid: str, limit_data: int, site_url: str, scrape_name: str, url_pattern: list[dict], space_rule: str):
        self.site_guid = site_guid
        self.account_guid = account_guid
        self.limit_data = limit_data
        self.scrape_name = scrape_name
        self.site_url = site_url
        self.url_pattern = url_pattern
        self.space_rule = space_rule
