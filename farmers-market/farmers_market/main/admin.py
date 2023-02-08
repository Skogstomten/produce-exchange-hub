from django.contrib import admin

from . import models


def register(model):
    admin.site.register(model)


register(models.Language)
register(models.CompanyType)
register(models.CompanyStatus)
register(models.ChangeType)
register(models.Company)
register(models.CompanyRole)
register(models.CompanyUser)
register(models.CompanyChange)
register(models.CompanyDescription)
register(models.Address)
register(models.ContactType)
register(models.Contact)
register(models.Product)
register(models.ProductName)
register(models.Order)
