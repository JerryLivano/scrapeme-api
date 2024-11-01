from abc import ABC, abstractmethod
from entities.scrape import Scrape

class IScrapRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_guid(self, guid: str):
        pass

    @abstractmethod
    def create(self, scrap: Scrape):
        pass