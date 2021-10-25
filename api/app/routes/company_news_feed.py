from fastapi import APIRouter, Depends, Path

from app.datastores.news_feed_datastore import NewsFeedDatastore, get_news_feed_datastore
from app.dependencies.app_headers import AppHeaders, get_headers
from app.models.api_list_response_model import ApiListResponseModel
from app.models.news_feed.news_feed_out_model import NewsFeedOutModel

router = APIRouter(
    prefix='/companies/{company_id}/news-feed'
)


@router.get('/', response_model=ApiListResponseModel[NewsFeedOutModel])
def get_news_feed(
        headers: AppHeaders = Depends(get_headers),
        company_id: str = Path(...),
        datastore: NewsFeedDatastore = Depends(get_news_feed_datastore)
):
    news_feed = datastore.get_news_feed(company_id, headers)
    return {'items': news_feed}


@router.get('/{post_id}', response_model=NewsFeedOutModel)
def get_news_feed_post(
        headers: AppHeaders = Depends(get_headers),
        company_id: str = Path(...),
        post_id: str = Path(...),
        datastore: NewsFeedDatastore = Depends(get_news_feed_datastore)
):
    return datastore.get_news_feed_post(company_id, post_id, headers)


# @router.post('/')
# def add_news_feed_post(
#         headers: App
# )
