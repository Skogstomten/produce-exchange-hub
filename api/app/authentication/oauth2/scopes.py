"""Scopes"""


class Scopes:
    """Contains a list of scopes."""

    def __init__(self, scopes: list[str]):
        """Creates scopes instance for scopes."""
        self._scopes = scopes

    def has_scope(self, scope: str) -> bool:
        """Checks if scope exists."""
        return scope in self._scopes
