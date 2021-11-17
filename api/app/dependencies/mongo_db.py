from pymongo import MongoClient
from pymongo.database import Database
from fastapi import Depends


def get_mongo_client() -> MongoClient:
    client = MongoClient(
        "mongodb+srv://produce_exchange_hub_api_dev:?x?x9e9h@7T45dNe@dev01.sokvl.mongodb.net/proruce_exchange_hub_dev"
        "?retryWrites=true&w=majority "
    )
    return client


def get_mongo_db(
        mongo_client: MongoClient = Depends(get_mongo_client)
) -> Database:
    return mongo_client.get_database()
