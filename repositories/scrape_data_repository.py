from pymongo.database import Database
from pymongo.errors import PyMongoError

from dto.dashboard.top_scraper_dto import TopScraperDto
from dto.scrape_data.update_fav_dto import UpdateFavDto
from dto.scrape_data.update_note_dto import UpdateNoteDto
from entities.scrape_data import ScrapeData


class ScrapeDataRepository:
    def __init__(self, db: Database):
        self._collection = db["scrape_data"]

    def get_top_scraper(self) -> list[TopScraperDto] | None:
        try:
            pipeline = [
                {
                    "$group": {
                        "account_guid": "$account_guid",
                        "count": {"$sum": 1}
                    }
                },
                {
                    "$sort": {"count": -1}
                },
                {
                    "$limit": 7
                },
                {
                    "$project": {
                        "account_guid": "$account_guid",
                        "count": 1,
                        "_id": 0
                    }
                }
            ]
            result = [TopScraperDto(
                data["account_guid"],
                data["count"]
            ) for data in self._collection.aggregate(pipeline)]
            return result
        except PyMongoError:
            return None

    def get_all(self) -> list[ScrapeData] | None:
        try:
            result = self._collection.find()
            return [ScrapeData(
                guid=data['guid'],
                account_guid=data['account_guid'],
                site_guid=data['site_guid'],
                scrape_name=data['scrape_name'],
                limit_data=data['limit_data'],
                data_count=data['data_count'],
                favourite_count=data['favourite_count'],
                web_data=data['web_data'],
                scrape_time=data['scrape_time'],
                created_date=data['created_date']
            ) for data in result]
        except PyMongoError:
            return None

    def get_by_guid(self, guid: str) -> ScrapeData | None:
        try:
            result = self._collection.find_one({"guid": guid})
            if not result:
                return None
            return ScrapeData(
                guid=result['guid'],
                account_guid=result['account_guid'],
                site_guid=result['site_guid'],
                scrape_name=result['scrape_name'],
                limit_data=result['limit_data'],
                data_count=result['data_count'],
                favourite_count=result['favourite_count'],
                web_data=result['web_data'],
                scrape_time=result['scrape_time'],
                created_date=result['created_date']
            )
        except PyMongoError:
            return None

    def create(self, scrape_data: ScrapeData) -> ScrapeData | None:
        try:
            result = self._collection.insert_one(scrape_data.to_dict())
            if not result:
                return None
            return scrape_data
        except PyMongoError:
            return None

    def update_favourite(self, request: UpdateFavDto) -> bool:
        try:
            result = self._collection.update_one(
                {"guid": request.guid},
                {"$set": {f"web_data[{request.index}].is_favourite": request.is_favourite}}
            )
            if not result:
                return False
            return True
        except PyMongoError:
            return False

    def update_note(self, request: UpdateNoteDto) -> bool:
        try:
            result = self._collection.update_one(
                {"guid": request.guid},
                {"$set": {f"web_data[{request.index}].note": request.note}}
            )
            if not result:
                return False
            return True
        except PyMongoError:
            return False
