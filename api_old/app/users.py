from flask import Blueprint

from app.database_access.users_datastore import UsersDatastore

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/', methods=('GET',))
def list_users():
    users = UsersDatastore().list_users()
    items = []
    for user in users:
        items.append(user.to_dict())

    response = {'items': items}
    return response
