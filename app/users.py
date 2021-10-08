from app.db import get_db, DocumentDatabase

from flask import Blueprint

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/', methods=('GET',))
def users():
    db_respons = get_db().list_users()
    items = []
    for row in db_respons:
        items.append(row.to_dict())

    response = {'items': items}
    return response
