from urllib.parse import quote_plus

from pymongo import MongoClient, ssl_support
from pymongo.database import Database
from fastapi import Depends


def get_mongo_client() -> MongoClient:
    client = MongoClient(f"mongodb+srv://{quote_plus('produce_exchange_hub_api_dev')}:{quote_plus('?x?x9e9h@7T45dNe')}"
                         f"@dev01.sokvl.mongodb.net/produce-exchange-hub-test?retryWrites=true&w=majority",
                         ssl_cert_reqs=ssl_support.CERT_NONE)
    return client
# produce_exchange_hub_api_dev
# ?x?x9e9h@7T45dNe


def get_mongo_db(
        mongo_client: MongoClient = Depends(get_mongo_client)
) -> Database:
    return mongo_client.get_database()
