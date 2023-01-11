from django.contrib import admin

from . import models

admin.site.register(models.Language)
admin.site.register(models.CompanyType)
admin.site.register(models.CompanyStatus)
admin.site.register(models.ChangeType)
admin.site.register(models.Company)
admin.site.register(models.CompanyRole)
admin.site.register(models.CompanyUser)
admin.site.register(models.CompanyChange)
admin.site.register(models.CompanyDescription)
admin.site.register(models.Address)
admin.site.register(models.ContactType)
admin.site.register(models.Contact)
admin.site.register(models.Product)
admin.site.register(models.ProductName)
admin.site.register(models.Currency)
admin.site.register(models.Order)
