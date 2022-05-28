from typing import Any, Type


class UserClaim(object):
    claim_type: str
    value_type: Type
    value: Any

    def __init__(self, claim_type: str, value_type: Type, value: Any):
        self.type = claim_type
        self.value_type = value_type
        self.value = value
        