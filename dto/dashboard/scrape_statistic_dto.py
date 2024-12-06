class ScrapeStatisticDto:
    def __init__(self, site_guid: str, months: dict):
        self.site_guid = site_guid
        self.months = months