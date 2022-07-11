from urllib.parse import quote_plus

import certifi
from pymongo import MongoClient


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


def get_local_mongo_client() -> MongoClient:
    """Returns a MongoClient for local mongo db."""
    client = MongoClient("mongodb://localhost:27017/produce_exchange_hub?retryWrites=true&w=majority")
    return client


def get_remote_collections():
    remote_db = get_mongo_client().get_database()
    collections = []
    for col in remote_db.list_collection_names():
        collections.append(remote_db.get_collection(col))
    return collections


def copy_to_local(remote_collections):
    local_db = get_local_mongo_client().get_database()
    for remote_collection in remote_collections:
        local_collection = local_db.get_collection(remote_collection.name)
        docs = remote_collection.find()
        local_collection.insert_many(docs)


def main():
    remote_collections = get_remote_collections()
    copy_to_local(remote_collections)


if __name__ == '__main__':
    main()
