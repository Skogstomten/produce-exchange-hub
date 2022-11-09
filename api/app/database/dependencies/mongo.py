"""
Module for MongoDB dependencies.
"""
import functools

from fastapi import Depends
from pymongo import MongoClient
from pymongo.database import Database


@functools.lru_cache(None)
def get_local_mongo_client() -> MongoClient:
    """Returns a MongoClient for local mongo db."""
    client = MongoClient("mongodb://localhost:27017/produce_exchange_hub?retryWrites=true&w=majority")
    return client


def get_mongo_db(
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
