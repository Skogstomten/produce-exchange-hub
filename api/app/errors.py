"""
Errors and exceptions
"""
from fastapi import HTTPException
from starlette import status


class ErrorModel:
    """
    Response model for errors.
    """

    status_code: int
    detail: str
    request_url: str

    def __init__(self, status_code: int, detail: str, request_url: str):
        """
        Creates an error model.
        :param status_code:
        :param detail:
        """
        super().__init__()
        self.status_code = status_code
        self.detail = detail
        self.request_url = request_url

    def dict(self) -> dict:
        return vars(self)


class DuplicateError(HTTPException):
    """
    Error raised when a call conflicts with some other data.
    For example if data is attempted to be added where a unique
    key is already in use.
    """

    def __init__(self, detail: str):
        """
        Creates error.
        :param detail: Message about what caused the error.
        Will be sent to caller as http response body.
        """
        super(DuplicateError, self).__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class InvalidOperationError(Exception):
    """
    Raised when an invalid operation is being performed.
    """

    def __init__(self, message: str):
        """Creates error."""
        super(InvalidOperationError, self).__init__(message)


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


class NotFoundError(HTTPException):
    """
    Raised if any resource is not found.
    """

    def __init__(self, detail: str):
        """Creates new instance."""
        super(NotFoundError, self).__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail
        )


class UnauthorizedError(HTTPException):
    """
    Raised if authenticated user is not authorized to access resource
    or operation they are attempting to access.
    """

    def __init__(self):
        """Creates UnauthorizedError."""
        super(UnauthorizedError, self).__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You're not authorized to perform this operation",
        )


class UnsupportedTimezoneError(HTTPException):
    """
    Raised if timezone header contains a value for timezone which is not
    supported.
    """

    def __init__(self, timezone: str):
        """Creates UnsupportedTimezoneError."""
        super(UnsupportedTimezoneError, self).__init__(
            status_code=400,
            detail=f"Timezone '{timezone}' is not supported. "
            f"List of available timezones can be found here: "
            f"",
        )
