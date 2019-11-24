from enum import Enum


class ConstantVariables(Enum):
    # MongoDB
    MONGO_PATH = "mongodb://localhost:27017/"
    DB_NAME = "scrape_db"
    QUOTE_COLLECTION_NAME = "quotes"
