# Generated by Django 4.1.3 on 2022-12-03 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_alter_company_activation_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="name",
            field=models.CharField(default="company_name", max_length=100),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="CompanyNames",
        ),
    ]
