"""
Claim
TODO: Can probably be moved into models.shared.
"""
from typing import Any

from pydantic import BaseModel

from app.shared.utils.string_values import StringValues


class Claim(BaseModel):
    """Claim model."""

    type: str
    value: Any

    def __init__(self, claim_type: str, value: Any):
        """Creates a claim."""
        super().__init__(type=claim_type, value=value)

    def get_value(self) -> Any:
        """Get claim value."""
        if isinstance(self.value, StringValues):
            return self.value.values
        return self.value
