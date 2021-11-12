from app.errors.not_found_error import NotFoundError


class CompanyNotFoundError(NotFoundError):
    def __init__(self, company_id: str):
        super(CompanyNotFoundError, self).__init__(f"Company with id '{company_id}' was not found")
