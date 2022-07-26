from fastapi import HTTPException, status


class InvalidInputError(HTTPException):
    """Raised when any input is invalid."""

    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
