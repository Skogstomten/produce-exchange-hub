from enum import Enum


class CompanyStatus(Enum, str):
    unactivated = 'unactivated'
    active = 'active'
