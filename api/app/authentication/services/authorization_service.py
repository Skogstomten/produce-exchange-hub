from app.database.enums import CompanyRole
from app.database.models import User, CompanyUser


def is_company_admin(user: User, company_id: int) -> bool:
    company_user = CompanyUser.get_or_none(
        CompanyUser.select().where(CompanyUser.company_id == company_id and CompanyUser.user_id == user.id)
    )
    return company_user.role == CompanyRole.company_admin
