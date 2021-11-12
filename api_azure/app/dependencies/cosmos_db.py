from azure.cosmos import CosmosClient, DatabaseProxy, ContainerProxy
from fastapi import Depends


def get_cosmos_client() -> CosmosClient:
    uri = 'https://produce-exchange-hub-api.documents.azure.com:443/'
    key = 'cKmACFBMoSFuAHugfUBRrEy5b4C4dmbJrSKaRNxyF96RPLpw8MLcyY5hBpdsuZiJJmL3b6jprd255Kh3X9mEGQ=='
    return CosmosClient(uri, credential=key)


def get_database_proxy(cosmos_client: CosmosClient = Depends(get_cosmos_client)) -> DatabaseProxy:
    db_name = 'produce-exchange-hub-api-db'
    return cosmos_client.get_database_client(db_name)


def get_container_proxy(database_proxy: DatabaseProxy = Depends(get_database_proxy)) -> ContainerProxy:
    return database_proxy.get_container_client('companies')
