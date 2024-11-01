from entities.scrape import Scrape
from repositories.interfaces.i_scrape_repository import IScrapRepository

class ScrapRepository(IScrapRepository):
    def __init__(self):
        self.data = []

    def get_all(self):
        return self.data

    def get_by_guid(self, guid: str):
        for item in self.data:
            if item.guid == guid:
                return item
        return None

    def create(self, scrap: Scrape):
        self.data.append(scrap)