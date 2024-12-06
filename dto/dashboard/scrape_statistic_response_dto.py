class ScrapeStatisticResponseDto:
    def __init__(self, site_name: str, months: dict):
        self.site_name = site_name
        self.months = months