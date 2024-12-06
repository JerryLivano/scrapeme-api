import os
import subprocess
import time
from datetime import datetime, timedelta
from pymongo.database import Database
from selenium.common import WebDriverException
from dto.scrape_data.create_site_url_dto import CreateSiteUrlDto
from dto.scrape_data.scrape_data_dto import ScrapeDataDto
from dto.scrape_data.scrape_data_request_dto import ScrapeDataRequestDto
from repositories.template_repository import TemplateRepository
from services.interfaces.i_parse_html_service import IParseHTMLService
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, Comment

from services.scrape_data_service import ScrapeDataService


class ParseHTMLService(IParseHTMLService):
    def __init__(self, db: Database):
        self.driver_path = self._get_driver_path()
        self._template_repository = TemplateRepository(db)
        self._scrape_service = ScrapeDataService(db)

    def _get_driver_path(self):
        project_root = os.path.dirname(os.path.abspath(__file__))
        driver_path = os.path.join(project_root, '../driver/chromedriver-win64/chromedriver.exe')
        return driver_path

    def _initialize_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-popup-blocking')

        service = Service(self.driver_path, port=0)
        return webdriver.Chrome(service=service, options=options)

    def kill_chromedriver(self):
        try:
            result = subprocess.run(
                ["tasklist"],
                stdout=subprocess.PIPE,
                text=True
            )
            if "chromedriver.exe" in result.stdout:
                os.system("taskkill /f /im chromedriver.exe")
        except Exception as e:
            print(f"Error while killing chromedriver: {e}")

    @staticmethod
    def create_site_url(request: CreateSiteUrlDto) -> str | None:
        try:
            result = (request.site_url + ("".join([
                f"{str(item['identifier'])}{f"{str(item.get('form_id')).replace(" ", request.space_rule)}" if item.get('form_id') else ""}"
                for item in request.url_pattern]))) if request.url_pattern else None
            return result
        except ValueError:
            return None

    def parse_html(self, url) -> BeautifulSoup | None:
        driver = None
        try:
            self.kill_chromedriver()
            driver = self._initialize_driver()

            driver.get(url)
            content = driver.page_source

            soup = BeautifulSoup(content, 'html.parser')

            comments = soup.find_all(string=lambda text: isinstance(text, Comment))
            for comment in comments:
                comment.extract()

            # divs = soup.find_all('div')
            # div_counts = {}
            #
            # for div in divs:
            #     child_divs = div.find_all('div', recursive=False)
            #     div_counts[div] = len(child_divs)
            #
            # result = max(div_counts, key=div_counts.get)

            return soup.body
        except WebDriverException as e:
            print(f"WebDriver error: {e}")
            return None
        finally:
            if driver:
                driver.quit()
            time.sleep(4)

    def scrape_data(self, request: ScrapeDataDto) -> list[dict] | int | None:
        try:
            start_time = time.time()
            limit_data = request.limit_data
            page = 1
            collected_data = 0

            template = self._template_repository.get_by_site_guid(request.site_guid)
            if not template:
                return -1

            scraped_data = []
            # List penyimpanan data scraping sementara
            temp_result = [[] for _ in template.tag_data]

            # Pengulangan untuk membatasi scraping data
            while collected_data < limit_data:
                # Membuat URL tiap page
                current_url_pattern = []
                for pattern in request.url_pattern:
                    if pattern.get('is_page', False):
                        current_url_pattern.append({
                            "identifier": pattern['identifier'],
                            "form_id": str(page),
                            "is_page": True
                        })
                    else:
                        current_url_pattern.append(pattern)

                url = self.create_site_url(CreateSiteUrlDto(
                    request.site_url,
                    current_url_pattern,
                    request.space_rule
                ))

                print(url)

                # Mengambil sumber HTML tiap URL
                soup = self.parse_html(url)
                if not soup:
                    print(f"Soup '{soup}' not found.")
                    break

                # Ambil kumpulan tag data berdasarkan container
                container = []
                if template.is_class:
                    container = soup.find_all(template.container_tag, class_=template.container)
                elif template.is_id:
                    container = soup.find_all(template.container_tag, id=template.container)

                if not container:
                    print(f"Container '{template.container}' not found.")
                    break

                # Ambil tag yang ada pada container dari template
                for item in container:
                    for idx, tag in enumerate(template.tag_data):
                        try:
                            if tag['type'] == "":
                                elements = item.find(tag['tag'])
                            else:
                                elements = item.find(tag['tag'], attrs={tag['type']: tag['identifier']})

                            temp_result[idx].append(elements)

                        except (AttributeError, KeyError, TypeError):
                            print(f"Error processing tag: {tag}")
                            continue

                # Hasil banyak data
                collected_data = len(temp_result[0])
                page += 1
                print(collected_data)

            # Membatasi banyak data berdasarkan limit
            for i in range(len(temp_result)):
                temp_result[i] = temp_result[i][:limit_data]

            num_items = len(temp_result[0])
            for i in range(num_items):
                # Membuat object data
                item_data = {
                    "index": i,
                    "is_favourite": False,
                    "note": ""
                }
                for idx, tag in enumerate(template.tag_data):
                    # Ambil element dari temp_result
                    element = temp_result[idx][i] if i < len(temp_result[idx]) else None
                    if element:
                        if tag.get("is_container", False):
                            # Ambil data dari list tag
                            if tag["child_type"] == "":
                                list_element = element.find_all(tag['child_tag'])
                            else:
                                list_element = element.find_all(tag['child_tag'],
                                                                attrs={tag['child_type']: tag['child_identifier']})

                            if tag["child_tag"].lower() == "img":
                                item_data[tag['title'].lower().replace(" ", "_")] = [elem.get('src', None) for elem in
                                                                                     list_element]
                            elif tag["child_tag"].lower() == "a":
                                hrefs = [elem.get('href', None) for elem in list_element]
                                for href in hrefs:
                                    if request.site_url[12:] not in href:
                                        item_data[tag['title'].lower().replace(" ", "_")] = f"{request.site_url}{href}"
                                    else:
                                        item_data[tag['title'].lower().replace(" ", "_")] = href
                            else:
                                list_title = [title.strip() for title in tag["title"].split(",")]
                                for j, elem in enumerate(list_element):
                                    if j < len(list_title):
                                        item_data[list_title[j].lower().replace(" ", "_")] = elem.get_text(strip=True,
                                                                                                           separator=" ").strip() if elem else None
                        # Ambil data dari tag
                        else:
                            if tag["tag"].lower() == "img":
                                item_data[tag['title'].lower().replace(" ", "_")] = element.get('src', None)
                            elif tag["tag"].lower() == "a":
                                href = element.get('href', None)
                                if request.site_url[12:] not in href:
                                    item_data[tag['title'].lower().replace(" ", "_")] = f"{request.site_url}{href}"
                                else:
                                    item_data[tag['title'].lower().replace(" ", "_")] = href
                            else:
                                item_data[tag['title'].lower().replace(" ", "_")] = element.get_text(strip=True,
                                                                                                     separator=" ").strip()
                    else:
                        item_data[tag['title'].lower().replace(" ", "_")] = None
                scraped_data.append(item_data)

            end_time = time.time()
            scrape_time = end_time - start_time
            hours, remainder = divmod(int(scrape_time), 3600)
            minutes, seconds = divmod(remainder, 60)

            # Add data ke database
            request_dto = ScrapeDataRequestDto(
                account_guid=request.account_guid,
                site_guid=request.site_guid,
                scrape_name=request.scrape_name if request.scrape_name != "" else (
                        datetime.utcnow() + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S"),
                data_count=len(scraped_data),
                web_data=scraped_data,
                scrape_time=f"{hours:02}:{minutes:02}:{seconds:02}"
            )
            result = self._scrape_service.create_scrape_data(request_dto)

            # Return hasil
            if not result:
                return 0
            return result.to_dict()

        except Exception as e:
            print(f"Error during scraping: {e}")
            return None
