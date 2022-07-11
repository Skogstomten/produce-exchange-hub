"""
Module for MongoDB dependencies.
"""
import functools
from urllib.parse import quote_plus

from pymongo import MongoClient
from pymongo.database import Database
from fastapi import Depends
import certifi


@functools.lru_cache(None)
def get_mongo_client() -> MongoClient:
    """
    Get the mongo client.
    Caches the client, since it can not be created more than once.
    :return: MongoClient.
    """
    client = MongoClient(
        f"mongodb+srv://{quote_plus('produce_exchange_hub_api_dev')}:"
        f"{quote_plus('?x?x9e9h@7T45dNe')}"
        "@dev01.sokvl.mongodb.net/produce-exchange-hub-test"
        "?retryWrites=true&w=majority",
        tlsCAFile=certifi.where(),
    )
    return client


@functools.lru_cache(None)
def get_local_mongo_client() -> MongoClient:
    """Returns a MongoClient for local mongo db."""
    client = MongoClient("mongodb://localhost:27017/produce_exchange_hub?retryWrites=true&w=majority")
    return client


def get_mongo_db(
    # mongo_client: MongoClient = Depends(get_mongo_client),
    mongo_client: MongoClient = Depends(get_local_mongo_client),
) -> Database:
    """
    DI method for database reference.
    This should never be directly injected into the datastores since
    they should not know about which database they are using.
    :param mongo_client: MongoClient.
    :return: Database.
    """
    return mongo_client.get_database()
