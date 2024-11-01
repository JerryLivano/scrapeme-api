import os
from entities.scrape import Scrape
from repositories.scrape_repository import ScrapRepository
from services.interfaces.i_scrape_service import IScrapService
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import uuid
import pandas as pd
import datetime

class ScrapService(IScrapService):
    def __init__(self):
        self.chrome_driver_path = self._get_driver_path()
        self.scrap_repository = ScrapRepository()
        self.driver = self._initialize_driver()

    def _get_driver_path(self):
        project_root = os.path.dirname(os.path.abspath(__file__))
        chrome_driver_path = os.path.join(project_root, '../chromedriver-win64/chromedriver.exe')
        return chrome_driver_path

    def _initialize_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-popup-blocking')

        service = Service(self.chrome_driver_path)
        return webdriver.Chrome(service=service, options=options)

    def parse_html(self, url):
        try:
            self.driver.get(url)

            content = self.driver.page_source

            soup = BeautifulSoup(content, 'html.parser')

            divs = soup.find_all('div')

            div_counts = {}

            for div in divs:
                child_divs = div.find_all('div', recursive=False)
                div_counts[div] = len(child_divs)

            max_div = max(div_counts, key=div_counts.get)

            return max_div.prettify()
        except Exception:
            return None
        finally:
            self.driver.quit()

    def scrap_data(self, url):
        self.driver.get(url)

        content = self.driver.page_source
        self.driver.quit()

        soup = BeautifulSoup(content, 'html.parser')

        for area in soup.find_all('div', class_ = 'featured-card-component'):
            try:
                name = area.find('h2').get_text()
                image = area.find('img')['src']
                price = area.find('div', class_='card-featured__middle-section__price').get_text()

                scrap_data = Scrape(uuid.uuid4(), name, image, price)
                self.scrap_repository.create(scrap_data)
            except AttributeError:
                continue

        return self.scrap_repository.get_all()

    def export_excel(self):
        try:
            datas = self.scrap_repository.get_all()

            result = {
                'Name': [data.name for data in datas],
                'Image': [data.image for data in datas],
                'Price': [data.price for data in datas]
            }

            df = pd.DataFrame(result)
            with pd.ExcelWriter(f"Scrap Data {datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx") as writer:
                df.to_excel(writer, index=False)

            return True
        except Exception:
            return False