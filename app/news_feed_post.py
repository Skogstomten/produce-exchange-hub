import datetime


class NewsFeedPost(object):
    id: str
    title: str

    def __init__(self, post_id: str, data: dict[str, dict], user_language: str):
        self.id = post_id
        self.title = data.get(user_language).get('title')
