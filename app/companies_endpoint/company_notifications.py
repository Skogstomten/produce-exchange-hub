from flask import Blueprint, request

from app.db import get_db

bp = Blueprint('company_notifications', __name__, url_prefix='/companies/<string:company_id>/notifications')


@bp.route('/', methods=('GET',))
def list_notifications(company_id: str):
    db = get_db()
    language = request.headers.get('language', 'SV')
    notifications = db.get_company_notifications(company_id, language)
    items = []
    for notification in notifications:
        items.append(notification.to_dict())

    return {
        'items': items
    }
