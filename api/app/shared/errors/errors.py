"""
Errors and exceptions
"""
from fastapi import HTTPException, status
from pydantic import BaseModel


class ErrorModel(BaseModel):
    """
    Response model for errors.
    """

    status_code: int
    detail: str
    request_url: str

    @classmethod
    def create(cls, status_code: int, detail: str, request_url: str):
        """Creates instance of ErrorModel."""
        return cls(status_code=status_code, detail=detail, request_url=request_url)


class InvalidOperationError(Exception):
    """
    Raised when an invalid operation is being performed.
    """

    def __init__(self, message: str):
        """Creates error."""
        super().__init__(message)


class NotFoundError(HTTPException):
    """
    Raised if any resource is not found.
    """

    def __init__(self, detail: str):
        """Creates new instance."""
        super(NotFoundError, self).__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UnsupportedTimezoneError(HTTPException):
    """
    Raised if timezone header contains a value for timezone which is not
    supported.
    """

    def __init__(self, timezone: str):
        """Creates UnsupportedTimezoneError."""
        super().__init__(
            status_code=400,
            detail=f"Timezone '{timezone}' is not supported. " f"List of available timezones can be found here: " f"",
        )
