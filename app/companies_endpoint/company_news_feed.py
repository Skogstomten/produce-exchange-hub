from flask import Blueprint, request
from datetime import datetime
from pytz import timezone

from app.db import get_db
from app.errors import NotFoundError
from app.response_helpers import not_found_response

bp = Blueprint('company_news_feed', __name__, url_prefix='/companies/<string:company_id>/news-feed')


@bp.route('/', methods=('GET',))
def list_news_feed(company_id: str):
    language = request.headers.get('language', 'SV')
    db = get_db()
    items = []
    for item in db.get_news_feed(company_id, language):
        items.append(item.to_dict())
    return {
        'items': items
    }


@bp.route('/', methods=('POST',))
def add_news_feed_post(company_id: str):
    language = request.headers.get('language', 'SV')

    user_id = request.json.get('user_id', None)
    post = request.json.get('post', None)
    date = datetime.now(timezone('Europe/Stockholm'))

    db = get_db()
    try:
        post_id = db.add_company_news_feed_post(
            company_id,
            user_id,
            post,
            date
        )
    except NotFoundError as err:
        return not_found_response(err)

    return db.get_news_feed_post(company_id, post_id, language).to_dict()
