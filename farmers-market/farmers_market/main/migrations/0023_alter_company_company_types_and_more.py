# Generated by Django 4.1.3 on 2023-01-03 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0022_alter_contact_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="company_types",
            field=models.ManyToManyField(blank=True, related_name="companies", to="main.companytype"),
        ),
        migrations.AlterField(
            model_name="company",
            name="content_languages",
            field=models.ManyToManyField(blank=True, related_name="companies", to="main.language"),
        ),
    ]
