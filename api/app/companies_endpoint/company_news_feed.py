from datetime import datetime

from flask import Blueprint, request, jsonify
from pytz import timezone

from app.database_access.news_feed_datastore import NewsFeedDatastore
from app.errors import NotFoundError
from app.response_helpers import not_found_response, make_response

bp = Blueprint('company_news_feed', __name__, url_prefix='/companies/<string:company_id>/news-feed')


@bp.route('/', methods=('GET',))
def list_news_feed(company_id: str):
    language = request.headers.get('language', 'SV')
    db = NewsFeedDatastore()
    items = []

    for item in db.list_news_feed(company_id, language):
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

    db = NewsFeedDatastore()
    try:
        post_id = db.add_news_feed_post(
            company_id,
            user_id,
            post,
            date
        )
    except NotFoundError as err:
        return not_found_response(err)

    new_post = db.get_news_feed_post(company_id, post_id, language).to_dict()
    return make_response(jsonify(new_post), 201)


@bp.route('/<string:post_id>', methods=('DELETE',))
def delete_news_feed_post(company_id: str, post_id: str):
    datastore = NewsFeedDatastore()
    datastore.delete_news_feed_post(company_id, post_id)

    return make_response(jsonify({}), 204)
