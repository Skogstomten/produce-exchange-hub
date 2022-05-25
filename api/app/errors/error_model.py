class ErrorModel(object):
    status_code: int
    detail: str

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

    def to_dict(self):
        return vars(self)
