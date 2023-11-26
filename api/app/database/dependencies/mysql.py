"""
Module for SQLAlchemy database engine injector.
"""
import functools

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase

CONNECTION_STRING = "mysql+mysqldb://root:Accountec1@localhost:3306/farmers_market"


class BaseModel(DeclarativeBase):
    pass


@functools.lru_cache(None)
def get_sqlalchemy_engine() -> Engine:
    """
    Return SQLAlchemy DB engine.
    """
    return create_engine(CONNECTION_STRING)
