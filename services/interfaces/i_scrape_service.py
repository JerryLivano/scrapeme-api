from abc import ABC, abstractmethod

class IScrapService(ABC):
    @abstractmethod
    def _initialize_driver(self):
        pass

    @abstractmethod
    def _get_driver_path(self):
        pass

    @abstractmethod
    def scrap_data(self, url):
        pass

    @abstractmethod
    def export_excel(self):
        pass
