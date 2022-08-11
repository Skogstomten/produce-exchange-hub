from fastapi import HTTPException, status


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
