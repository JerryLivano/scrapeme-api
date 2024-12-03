class UpdateNameDto:
    def __init__(self, guid: str, scrape_name: str):
        self.guid = guid
        self.scrape_name = scrape_name