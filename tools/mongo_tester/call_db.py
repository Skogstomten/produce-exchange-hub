from urllib.parse import quote_plus

from pymongo import ssl_support, MongoClient
from pymongo.collection import Collection

password = quote_plus('?x?x9e9h@7T45dNe')

client = MongoClient(
    f"mongodb+srv://produce_exchange_hub_api_dev:{password}@dev01.sokvl.mongodb.net/produce-exchange-hub-test?retryWrites=true&w=majority",
    ssl_cert_reqs=ssl_support.CERT_NONE
)
db = client.get_database()
companies: Collection = db.get_collection('companies')

for doc in companies.find():
    print(doc)
