from fastapi import HTTPException


class UsernameExistsError(HTTPException):
    def __init__(self, username: str):
        super(UsernameExistsError, self).__init__(400, f"Username '{username}' already exists")
