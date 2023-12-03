from enum import Enum, unique


@unique
class Currency(Enum):
    SEK = "SEK"
    EUR = "EUR"


@unique
class SortOrder(Enum):
    """Sort order."""

    asc = "asc"
    desc = "desc"
