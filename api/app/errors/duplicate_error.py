from fastapi import HTTPException, status


class DuplicateError(HTTPException):
    def __init__(self, detail: str):
        super(DuplicateError, self).__init__(
            status_code = status.HTTP_409_CONFLICT,
            detail=detail,
        )
