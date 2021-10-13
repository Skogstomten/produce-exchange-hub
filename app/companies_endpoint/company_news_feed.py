from flask import Blueprint, request

from app.db import get_db

bp = Blueprint('company_news_feed', __name__, url_prefix='/companies/<string:company_id>/news_feed')


@bp.route('/', methods=('GET',))
def news_feed(company_id: str):
    language = request.headers.get('language', 'SV')
    db = get_db()
    items = []
    for item in db.get_news_feed(company_id, language):
        items.append(item.to_dict())
    return {
        'items': items
    }
