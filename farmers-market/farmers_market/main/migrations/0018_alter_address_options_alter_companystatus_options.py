# Generated by Django 4.1.3 on 2022-12-24 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0017_alter_company_status"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="address",
            options={"verbose_name": "Address", "verbose_name_plural": "Addresses"},
        ),
        migrations.AlterModelOptions(
            name="companystatus",
            options={
                "verbose_name": "CompanyStatus",
                "verbose_name_plural": "CompanyStatuses",
            },
        ),
    ]
