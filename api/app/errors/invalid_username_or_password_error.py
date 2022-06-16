from fastapi import HTTPException, status


class InvalidUsernameOrPasswordError(HTTPException):
    def __init__(self):
        super(InvalidUsernameOrPasswordError, self).__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
