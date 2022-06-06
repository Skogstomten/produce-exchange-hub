from typing import Any

from pydantic import BaseModel

from app.utils.string_values import StringValues


class Claim(BaseModel):
    type: str
    value: Any

    def __init__(self, claim_type: str, value: Any):
        super().__init__(type=claim_type, value=value)

    def get_value(self) -> Any:
        if isinstance(self.value, StringValues):
            return self.value.values
        return self.value
