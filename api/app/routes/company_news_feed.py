from fastapi import APIRouter, Depends, Path, Body

from app.datastores.news_feed_datastore import NewsFeedDatastore, get_news_feed_datastore
from app.dependencies.app_headers import AppHeaders, get_headers
from app.models.api_list_response_model import ApiListResponseModel
from app.models.companies.news_feed.news_feed_brief_out_model import NewsFeedBriefOutModel
from app.models.companies.news_feed.news_feed_out_model import NewsFeedOutModel

from app.models.companies.news_feed.news_feed_in_model import NewsFeedPostPutModel

router = APIRouter(
    prefix='/companies/{company_id}/news-feed'
)


@router.get('/', response_model=ApiListResponseModel[NewsFeedBriefOutModel])
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


@router.post('/', response_model=NewsFeedOutModel, status_code=201)
def add_news_feed_post(
        headers: AppHeaders = Depends(get_headers),
        company_id: str = Path(...),
        body: NewsFeedPostPutModel = Body(...),
        datastore: NewsFeedDatastore = Depends(get_news_feed_datastore)
):
    return datastore.add_news_feed_post(company_id, headers, body)


@router.put('/{post_id}', response_model=NewsFeedOutModel)
def update_news_feed_post(
        headers: AppHeaders = Depends(get_headers),
        company_id: str = Path(...),
        post_id: str = Path(...),
        body: NewsFeedPostPutModel = Body(...),
        datastore: NewsFeedDatastore = Depends(get_news_feed_datastore)
):
    return datastore.update_news_feed_post(company_id, post_id, body, headers)


@router.delete('/{post_id}', status_code=204)
def delete_news_feed_post(
        headers: AppHeaders = Depends(get_headers),
        company_id: str = Path(...),
        post_id: str = Path(...),
        datastore: NewsFeedDatastore = Depends(get_news_feed_datastore)
):
    datastore.delete_news_feed_post(company_id, post_id)
    return
