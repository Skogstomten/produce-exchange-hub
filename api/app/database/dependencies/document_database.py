# """
# Document database dependenciy.
# """
# from fastapi import Depends
# from pymongo.database import Database as MongoDatabase
#
# from app.logging.log import AppLoggerInjector, AppLogger
# from app.database.dependencies.mongo import get_mongo_db
# from app.database.abstract.document_database import DocumentDatabase
# from app.database.mongo.mongo_document_database import MongoDocumentDatabase
#
# logger_injector = AppLoggerInjector("MongoDocumentDatabase")
#
#
# def get_document_database(
#     db: MongoDatabase = Depends(get_mongo_db),
#     logger: AppLogger = Depends(logger_injector),
# ) -> DocumentDatabase:
#     """
#     Get document database reference.
#     Abstracts away actual underlying database engine.
#     :param db: Reference to db client. MongoDB in this case.
#     :param logger: AppLogger instance.
#     :return: New MongoDocumentDatabase which implements DocumentDatabase
#     interface.
#     """
#     return MongoDocumentDatabase(db, logger)
