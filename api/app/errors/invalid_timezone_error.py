from fastapi import HTTPException


class InvalidTimezoneError(HTTPException):
    def __init__(self, invalid_timezone: str):
        super(InvalidTimezoneError, self).__init__(400, f"Timezone '{invalid_timezone}' is invalid")
