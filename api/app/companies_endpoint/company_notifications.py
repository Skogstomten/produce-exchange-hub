from flask import Blueprint, request

from app.database_access.notifications_datastore import NotificationsDatastore

bp = Blueprint('company_notifications', __name__, url_prefix='/companies/<string:company_id>/notifications')


@bp.route('/', methods=('GET',))
def list_notifications(company_id: str):
    db = NotificationsDatastore()
    language = request.headers.get('language', 'SV')
    items = []

    for notification in db.get_company_notifications(company_id, language):
        items.append(notification.to_dict())

    return {
        'items': items
    }
