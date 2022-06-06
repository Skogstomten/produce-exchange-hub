from fastapi import HTTPException, status


class UnauthorizedError(HTTPException):
    def __init__(self):
        super(UnauthorizedError, self).__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You're not authorized to perform this operation",
        )
