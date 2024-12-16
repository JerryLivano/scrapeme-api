class ScrapeStatisticDto:
    def __init__(self, site_guid: str, count: int):
        self.site_guid = site_guid
        self.count = count