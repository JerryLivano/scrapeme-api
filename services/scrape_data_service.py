import re
import copy
from datetime import datetime, timedelta
from uuid import uuid4
from pymongo.database import Database
from pymongo.errors import PyMongoError
from dto.scrape_data.data_analysis_dto import DataAnalysisDto
from dto.scrape_data.get_scrape_dto import GetScrapeDto
from dto.scrape_data.location_comparison_dto import LocationComparisonDto
from dto.scrape_data.room_comparison_dto import RoomComparisonDto
from dto.scrape_data.scrape_data_request_dto import ScrapeDataRequestDto
from dto.scrape_data.update_fav_dto import UpdateFavDto
from dto.scrape_data.update_name_dto import UpdateNameDto
from dto.scrape_data.update_note_dto import UpdateNoteDto
from dto.scrape_data.web_data_analysis_dto import WebDataAnalysisDto
from entities.scrape_data import ScrapeData
from handlers.pagination.pagination_handler import PaginationHandler
from handlers.pagination.response_pagination_handler import ResponsePaginationHandler
from repositories.scrape_data_repository import ScrapeDataRepository
from repositories.site_repository import SiteRepository
from services.interfaces.i_scrape_data_service import IScrapeDataService


class ScrapeDataService(IScrapeDataService):
    def __init__(self, db: Database):
        self._scrape_data_repository = ScrapeDataRepository(db)
        self._site_repository = SiteRepository(db)

    @staticmethod
    def average(data, key) -> int | None:
        values = []
        for item in data:
            value = item.get(key, "-")
            match = re.search(r"(\d+[.,]?\d*)", value)
            if match:
                numeric_value = match.group(1).replace(',', '.')
                values.append(float(numeric_value))
        return int(sum(values) / len(values)) if values else None

    def get_data_analysis(self, account_guid: str, location: str, site_guid: str) -> DataAnalysisDto | None:
        try:
            if site_guid != "":
                scrape_data = self._scrape_data_repository.get_by_site(account_guid, site_guid)
            else:
                scrape_data = self._scrape_data_repository.get_by_account(account_guid)

            if len(scrape_data) == 0 or not scrape_data:
                return None

            result = []
            for item in scrape_data:
                result.extend(item.web_data)

            result = [item for item in result if (location.lower() in item.get("location", "").lower())]

            return DataAnalysisDto(
                avg_bedroom=self.average(result, "bedroom"),
                avg_bathroom=self.average(result, "bathroom"),
                avg_surface=self.average(result, "surface"),
                avg_building=self.average(result, "building")
            )
        except PyMongoError:
            return None

    def get_comparison(self, account_guid: str, location: str, site_guid: str, room: str) -> RoomComparisonDto | None:
        try:
            if room == "":
                return None

            if site_guid != "":
                scrape_data = self._scrape_data_repository.get_by_site(account_guid, site_guid)
            else:
                scrape_data = self._scrape_data_repository.get_by_account(account_guid)

            if len(scrape_data) == 0 or not scrape_data:
                return None

            result = []
            for item in scrape_data:
                result.extend(item.web_data)

            result = [item for item in result if (location.lower() in item.get("location", "").lower())]

            for item in result:
                values = item.get(room, "0")
                match = re.search(r"(\d+)", values)
                if match:
                    item[room] = int(match.group(1))
                else:
                    item[room] = 0

            highest = max(item.get(room, 0) for item in result)

            room_count = ["No Data" if i == 0 else f"{i} room" for i in range(0, highest + 1)]
            data_count = [0] * len(room_count)
            for item in result:
                value = item.get(room, 0)
                if value < len(data_count):
                    data_count[value] += 1

            return RoomComparisonDto(
                room=room_count[:10],
                count=data_count[:10]
            )
        except PyMongoError:
            return None

    def get_location_comparison(self, account_guid: str, site_guid: str, location_data: list[str]) -> list[
                                LocationComparisonDto] | None:
        try:
            if site_guid != "":
                scrape_data = self._scrape_data_repository.get_by_site(account_guid, site_guid)
            else:
                scrape_data = self._scrape_data_repository.get_by_account(account_guid)

            if len(scrape_data) == 0 or not scrape_data:
                return None

            result = []
            for item in scrape_data:
                result.extend(item.web_data)

            if len(location_data) == 0:
                return [LocationComparisonDto(
                    label="Other",
                    value=len(result)
                )]
            else:
                selected_count = 0
                data_count = [0] * len(location_data)
                for item in result:
                    location_value = item.get("location", "").lower()
                    for idx, location in enumerate(location_data):
                        if location.lower() in location_value:
                            data_count[idx] += 1
                            selected_count += 1
                            break
                other_count = len(result) - selected_count
                location_data = [data.capitalize() for data in location_data]
                location_data.append("Other")
                data_count.append(other_count)

                return [LocationComparisonDto(
                    label=item,
                    value=data_count[idx]
                ) for idx, item in enumerate(location_data)]
        except PyMongoError:
            return None

    def get_web_data_analysis(self, account_guid: str, location: str, site_guid: str,
                              order_by: str) -> WebDataAnalysisDto | None:
        try:
            if order_by == "":
                return None

            if site_guid != "":
                scrape_data = self._scrape_data_repository.get_by_site(account_guid, site_guid)
            else:
                scrape_data = self._scrape_data_repository.get_by_account(account_guid)

            if len(scrape_data) == 0 or not scrape_data:
                return None

            result = []
            for item in scrape_data:
                result.extend(item.web_data)

            result = [item for item in result if (location.lower() in item.get("location", "").lower())]
            mod_result = copy.deepcopy(result)

            for item in mod_result:
                for key in ["bedroom", "bathroom", "surface", "building"]:
                    value = item.get(key, "-")
                    if value == "-":
                        item[key] = None
                    else:
                        match = re.search(r"(\d+[.,]?\d*)", str(value))
                        item[key] = int(float(match.group(1))) if match else None

            if order_by == "asc":
                order_bedroom = max((
                    item.get("bedroom", 0) for item in mod_result if item.get("bedroom") is not None), default=None)
                order_bathroom = max((
                    item.get("bathroom", 0) for item in mod_result if item.get("bathroom") is not None), default=None)
                order_surface = max((
                    item.get("surface", 0) for item in mod_result if item.get("surface") is not None), default=None)
                order_building = max((
                    item.get("building", 0) for item in mod_result if item.get("building") is not None), default=None)
            else:
                order_bedroom = min((
                    item.get("bedroom", 999999) for item in mod_result if item.get("bedroom") is not None),
                    default=None)
                order_bathroom = min((
                    item.get("bathroom", 999999) for item in mod_result if item.get("bathroom") is not None),
                    default=None)
                order_surface = min((
                    item.get("surface", 999999) for item in mod_result if item.get("surface") is not None),
                    default=None)
                order_building = min((
                    item.get("building", 999999) for item in mod_result if item.get("building") is not None),
                    default=None)

            bedroom_data = []
            bathroom_data = []
            surface_data = []
            building_data = []

            for idx, item in enumerate(mod_result):
                if len(bedroom_data) == 0:
                    if order_bedroom is not None and item.get("bedroom", 0) == order_bedroom:
                        bedroom_data.append(result[idx])
                if len(bathroom_data) == 0:
                    if order_bathroom is not None and item.get("bathroom", 0) == order_bathroom:
                        bathroom_data.append(result[idx])
                if len(surface_data) == 0:
                    if order_surface is not None and item.get("surface", 0) == order_surface:
                        surface_data.append(result[idx])
                if len(building_data) == 0:
                    if order_building is not None and item.get("building", 0) == order_building:
                        building_data.append(result[idx])
                if len(bedroom_data) > 0 and len(bathroom_data) > 0 and len(surface_data) > 0 and len(
                        building_data) > 0:
                    break

            return WebDataAnalysisDto(
                sort_bedroom=bedroom_data,
                sort_bathroom=bathroom_data,
                sort_surface=surface_data,
                sort_building=building_data
            )
        except PyMongoError:
            return None

    def get_by_account(self, account_guid: str, search: str, page: int, limit: int, order_by: int,
                       column_name: str, site_guid: str | None) -> ResponsePaginationHandler | None:
        try:
            result = self._scrape_data_repository.get_by_account(account_guid)

            result = [item for item in result if
                      (search.lower() in item.scrape_name.lower())]

            if column_name:
                if int(order_by) == 1:
                    result.sort(key=lambda x: getattr(x, column_name))
                elif int(order_by) == 2:
                    result.sort(key=lambda x: getattr(x, column_name), reverse=True)

            if site_guid:
                result = list(filter(lambda x: str(x.site_guid) == site_guid, result))

            if int(order_by) == 0:
                result.sort(key=lambda x: getattr(x, "created_date"), reverse=True)

            result = [GetScrapeDto(
                guid=data.guid,
                account_guid=data.account_guid,
                site_guid=data.site_guid,
                site_name=self._site_repository.get_by_guid(data.site_guid).site_name,
                scrape_name=data.scrape_name,
                data_count=data.data_count,
                favourite_count=data.favourite_count,
                web_data=data.web_data,
                scrape_time=data.scrape_time,
                created_date=data.created_date
            ) for data in result]

            return PaginationHandler.paginate(
                queryable=result,
                transform_function=lambda scrape_data, index: scrape_data.__dict__,
                page=page,
                limit=limit
            )
        except PyMongoError:
            return None

    def create_scrape_data(self, request: ScrapeDataRequestDto) -> ScrapeData | None:
        try:
            new_scrape_data = ScrapeData(
                str(uuid4()),
                request.account_guid,
                request.site_guid,
                request.scrape_name,
                request.data_count,
                0,
                request.web_data,
                request.scrape_time,
                datetime.utcnow() + timedelta(hours=7)
            )
            result = self._scrape_data_repository.create(new_scrape_data)
            if not result:
                return None
            return result
        except PyMongoError:
            return None

    def get_all_web_data(self, guid: str, search: str, page: int, limit: int, order_by: int,
                         column_name: str) -> ResponsePaginationHandler | None:
        try:
            result = self._scrape_data_repository.get_by_guid(guid).web_data

            if search:
                result = [web_data for web_data in result if
                          any(search.lower() in str(value).lower() for value in web_data.values())]

            if column_name:
                if int(order_by) == 1:
                    result.sort(key=lambda x: x[column_name])
                elif int(order_by) == 2:
                    result.sort(key=lambda x: x[column_name], reverse=True)

            return PaginationHandler.paginate(
                queryable=result,
                transform_function=lambda web_data, index: web_data,
                page=page,
                limit=limit
            )
        except PyMongoError:
            return None

    def get_fav_scrape_data(self, account_guid: str, search: str, page: int, limit: int, order_by: int,
                            column_name: str, site_guid: str | None) -> ResponsePaginationHandler | None:
        try:
            result = self._scrape_data_repository.get_by_account(account_guid)

            result = list(filter(lambda x: x.favourite_count > 0, result))

            result = [item for item in result if
                      (search.lower() in item.scrape_name.lower())]

            if column_name:
                if int(order_by) == 1:
                    result.sort(key=lambda x: getattr(x, column_name))
                elif int(order_by) == 2:
                    result.sort(key=lambda x: getattr(x, column_name), reverse=True)

            if site_guid:
                result = list(filter(lambda x: str(x.site_guid) == site_guid, result))

            if int(order_by) == 0:
                result.sort(key=lambda x: getattr(x, "created_date"), reverse=True)

            result = [GetScrapeDto(
                guid=data.guid,
                account_guid=data.account_guid,
                site_guid=data.site_guid,
                site_name=self._site_repository.get_by_guid(data.site_guid).site_name,
                scrape_name=data.scrape_name,
                data_count=data.data_count,
                favourite_count=data.favourite_count,
                web_data=data.web_data,
                scrape_time=data.scrape_time,
                created_date=data.created_date
            ) for data in result]

            return PaginationHandler.paginate(
                queryable=result,
                transform_function=lambda scrape_data, index: scrape_data.__dict__,
                page=page,
                limit=limit
            )
        except PyMongoError:
            return None

    def get_all_fav_web_data(self, guid: str, search: str, page: int, limit: int, order_by: int,
                             column_name: str) -> ResponsePaginationHandler | None:
        try:
            result = self._scrape_data_repository.get_by_guid(guid).web_data

            result = list(filter(lambda x: x["is_favourite"] == True, result))

            if search:
                result = [web_data for web_data in result if
                          any(search.lower() in str(value).lower() for value in web_data.values())]

            if column_name:
                if int(order_by) == 1:
                    result.sort(key=lambda x: x[column_name])
                elif int(order_by) == 2:
                    result.sort(key=lambda x: x[column_name], reverse=True)

            return PaginationHandler.paginate(
                queryable=result,
                transform_function=lambda web_data, index: web_data,
                page=page,
                limit=limit
            )
        except PyMongoError:
            return None

    def update_fav(self, request: UpdateFavDto) -> int:
        try:
            result = self._scrape_data_repository.update_favourite(request)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1

    def update_note(self, request: UpdateNoteDto) -> int:
        try:
            result = self._scrape_data_repository.update_note(request)
            if not result:
                return 0
            return 1
        except PyMongoError:
            return -1

    def update_scrape(self, request: UpdateNameDto) -> bool:
        try:
            result = self._scrape_data_repository.update_name(request)
            return result
        except PyMongoError:
            return False

    def delete_scrape(self, guid: str) -> bool:
        try:
            result = self._scrape_data_repository.delete(guid)
            return result
        except PyMongoError:
            return False
