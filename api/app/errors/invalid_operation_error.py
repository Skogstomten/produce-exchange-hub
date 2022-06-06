class InvalidOperationError(Exception):
    def __init__(self, message: str):
        super(InvalidOperationError, self).__init__(message)
