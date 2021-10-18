class NotFoundError(Exception):
    message: str

    def __init__(self, document_id: str):
        super().__init__(f"No document found with id '{document_id}'")
        self.message = f"No document found with id '{document_id}'"


class UnexpectedError(Exception):
    message: str

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidOperationError(UnexpectedError):
    pass
