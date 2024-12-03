import os
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class WebdriverMiddleware:
    def driver_path(self) -> str | None:
        project_root = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(project_root, '../driver/chromedriver-win64/chromedriver.exe')

    def initialize_driver(self):
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-popup-blocking')
            service = Service(self.driver_path())
            return webdriver.Chrome(service=service, options=options)
        except WebDriverException:
            return None