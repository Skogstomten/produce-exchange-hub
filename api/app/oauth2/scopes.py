"""Scopes"""


class Scopes:
    """TODO: Move to models.shared."""

    def __init__(self, scopes: list[str]):
        """Creates scopes instance for scopes."""
        self._scopes = scopes

    def has_scope(self, scope: str) -> bool:
        """Checks if scope exists."""
        return scope in self._scopes
