from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, message: str):
        super(NotFoundError, self).__init__(status_code=404, detail=message)
