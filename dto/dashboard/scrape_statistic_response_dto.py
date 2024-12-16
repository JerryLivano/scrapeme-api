class ScrapeStatisticResponseDto:
    def __init__(self, site_name: str, count: int):
        self.label = site_name
        self.value = count