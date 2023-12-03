import functools

from peewee import MySQLDatabase, Model


@functools.lru_cache(None)
def get_db():
    db = MySQLDatabase("produce_exchange_hub", user="root", password="Accountec1", host="localhost", port=3306)
    return db


class BaseModel(Model):
    class Meta:
        database = get_db()
