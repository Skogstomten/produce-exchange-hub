from fastapi import Header


class User(object):
    user_id: str

    def __init__(self, user_id: str):
        self.user_id = user_id


def get_user(user_id: str = Header(...)) -> User:
    return User(user_id)
