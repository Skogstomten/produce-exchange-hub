from fastapi import HTTPException, status


class ClaimTypeNotSupportedError(HTTPException):
    """Raises internally when claim type is wrong."""

    def __init__(self, claim_type: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Claim type '{claim_type}' is not supported",
        )
