from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, detail: str):
        super(NotFoundError, self).__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )
