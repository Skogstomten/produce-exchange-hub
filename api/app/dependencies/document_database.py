from fastapi import Depends
from pymongo.database import Database as MongoDatabase

from .mongo import get_mongo_db
from ..database.document_database import DocumentDatabase
from ..database.mongo.mongo_document_database import MongoDocumentDatabase


def get_document_database(db: MongoDatabase = Depends(get_mongo_db)) -> DocumentDatabase:
    return MongoDocumentDatabase(db)
