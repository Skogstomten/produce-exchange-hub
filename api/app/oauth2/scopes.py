class Scopes:
    def __init__(self, scopes: list[str]):
        self._scopes = scopes

    def has_scope(self, scope: str) -> bool:
        return scope in self._scopes
