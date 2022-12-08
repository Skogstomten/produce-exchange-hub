# Generated by Django 4.1.3 on 2022-12-08 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_alter_companyuser_company_alter_contact_company"),
    ]

    operations = [
        migrations.AddField(
            model_name="companytype",
            name="type_name_en",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="companytype",
            name="type_name_sv",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="language",
            name="name_en",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="language",
            name="name_sv",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
