from fastapi import HTTPException


class UnsupportedTimezoneError(HTTPException):
    def __init__(self, timezone: str):
        super(UnsupportedTimezoneError, self).__init__(
            status_code=400,
            detail=f"Timezone '{timezone}' is not supported. "
                   f"List of available timezones can be found here: "
                   f""
        )
