import functools
from urllib.parse import quote_plus

from pymongo import MongoClient
from pymongo.database import Database
from fastapi import Depends
import certifi


@functools.lru_cache(None)
def get_mongo_client() -> MongoClient:
    client = MongoClient(f"mongodb+srv://{quote_plus('produce_exchange_hub_api_dev')}:{quote_plus('?x?x9e9h@7T45dNe')}"
                         f"@dev01.sokvl.mongodb.net/produce-exchange-hub-test?retryWrites=true&w=majority",
                         tlsCAFile=certifi.where())
    return client


# produce_exchange_hub_api_dev
# ?x?x9e9h@7T45dNe


def get_mongo_db(
        mongo_client: MongoClient = Depends(get_mongo_client)
) -> Database:
    return mongo_client.get_database()
