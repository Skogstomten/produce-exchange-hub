from sqlalchemy import create_engine

CONNECTION_STRING = "mysql+mysqldb://root:Accountec1@localhost:3306/farmers_market"

engine = create_engine(CONNECTION_STRING)


def get_sqlalchemy_engine():
    return engine
