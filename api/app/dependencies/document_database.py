"""
Document database dependenciy.
"""
from fastapi import Depends
from pymongo.database import Database as MongoDatabase

from .mongo import get_mongo_db
from ..database.document_database import DocumentDatabase
from ..database.mongo.mongo_document_database import MongoDocumentDatabase


def get_document_database(
    db: MongoDatabase = Depends(get_mongo_db),
) -> DocumentDatabase:
    """
    Get document database reference.
    Abstracts away actual underlying database engine.
    :param db: Reference to db client. MongoDB in this case.
    :return: New MongoDocumentDatabase which implements DocumentDatabase
    interface.
    """
    return MongoDocumentDatabase(db)
