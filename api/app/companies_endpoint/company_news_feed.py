from datetime import datetime

from flask import Blueprint, request, jsonify
from jsonschema import validate
from pytz import timezone

from app.database_access.news_feed_datastore import NewsFeedDatastore
from app.response_helpers import make_response, updated_response

bp = Blueprint('company_news_feed', __name__, url_prefix='/companies/<string:company_id>/news-feed')

news_feed_input_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'post': {
            'type': 'array',
            'contains': {
                'type': 'object',
                'properties': {
                    'language_iso': {'type': 'string', 'minLength': 2, 'maxLength': 2},
                    'title': {'type': 'string'},
                    'body': {'type': 'string'},
                },
            },
            'minContains': 1,
        },
    },
}


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

    validate(instance=request.json, schema=news_feed_input_schema)

    user_id = request.json.get('user_id', None)
    post = request.json.get('post', None)
    date = datetime.now(timezone('Europe/Stockholm'))

    db = NewsFeedDatastore()
    post_id = db.add_news_feed_post(
        company_id,
        user_id,
        post,
        date
    )

    new_post = db.get_news_feed_post(company_id, post_id, language).to_dict()
    return make_response(jsonify(new_post), 201)


@bp.route('/<string:post_id>/', methods=('PUT',))
def update_news_feed_post(company_id: str, post_id: str):
    language = request.headers.get('language', 'SV')

    validate(instance=request.json, schema=news_feed_input_schema)

    user_id = request.json.get('user_id', None)
    post = request.json.get('post', None)

    datastore = NewsFeedDatastore()
    updated_post = datastore.update_post(company_id, post_id, user_id, post, language)

    return updated_response(updated_post.to_dict())


@bp.route('/<string:post_id>', methods=('DELETE',))
def delete_news_feed_post(company_id: str, post_id: str):
    datastore = NewsFeedDatastore()
    datastore.delete_news_feed_post(company_id, post_id)

    return make_response(jsonify({}), 204)
