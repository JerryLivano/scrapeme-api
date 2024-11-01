from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, uri="mongodb://localhost:27017", db = "db_scrape"):
        self.client = MongoClient(uri)
        self.db = self.client[db]

    def get_database(self):
        return self.db