from fastapi import HTTPException


class EmailExistsError(HTTPException):
    def __init__(self, email: str):
        super(EmailExistsError, self).__init__(400, f"Email '{email}' is already in use")
