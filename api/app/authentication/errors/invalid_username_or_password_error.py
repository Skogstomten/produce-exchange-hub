from fastapi import HTTPException, status


class InvalidUsernameOrPasswordError(HTTPException):
    """
    Raised if username or password is invalid when authenticating.
    """

    def __init__(self):
        """Creates instance."""
        super(InvalidUsernameOrPasswordError, self).__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
