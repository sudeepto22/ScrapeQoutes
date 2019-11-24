from pymongo import MongoClient


class MongoConnection(object):
    def __init__(self, mongo_url: str, mongo_db_name: str, mongo_collection_name: str):
        self.mongo_url = mongo_url
        self.mongo_db_name = mongo_db_name
        self.mongo_collection_name = mongo_collection_name

        self.collection = None

    def connect_mongo(self):
        client = MongoClient(self.mongo_url)
        db = client[self.mongo_db_name]
        self.collection = db[self.mongo_collection_name]

    def insert_many(self, data):
        self.collection.insert_many(data)
