from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from dto.scrape_data.create_site_url_dto import CreateSiteUrlDto
from dto.scrape_data.scrape_data_dto import ScrapeDataDto
from dto.scrape_data.scrape_result_dto import ScrapeResultDto


class IParseHTMLService(ABC):
    @abstractmethod
    def _get_driver_path(self):
        pass

    @abstractmethod
    def _initialize_driver(self):
        pass

    @abstractmethod
    def kill_chromedriver(self):
        pass

    @abstractmethod
    def get_html_source(self, url) -> BeautifulSoup | None:
        pass

    @abstractmethod
    def scrape_data(self, request: ScrapeDataDto) -> ScrapeResultDto | int | None:
        pass
