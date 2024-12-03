from abc import ABC, abstractmethod

class IParseHTMLService(ABC):
    @abstractmethod
    def _initialize_driver(self):
        pass

    @abstractmethod
    def _get_driver_path(self):
        pass

    @abstractmethod
    def parse_html(self, url):
        pass
