from flask import Blueprint

from app.database_access.news_feed_datastore import NewsFeedDatastore

bp = Blueprint('companies_news_feed_raw', __name__, url_prefix='/companies/<string:company_id>/news-feed-raw')


@bp.route('/', methods=('GET',))
def list_news_feed_raw(company_id: str):
    datastore = NewsFeedDatastore()
    posts = datastore.get_news_feed_raw(company_id)
    return {'items': list(posts)}
