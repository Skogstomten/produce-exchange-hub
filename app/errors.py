class NotFoundError(Exception):
    message: str

    def __init__(self, document_id: str):
        super().__init__(f"No document found with id '{document_id}'")
        self.message = f"No document found with id '{document_id}'"
