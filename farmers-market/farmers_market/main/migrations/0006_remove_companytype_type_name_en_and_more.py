# Generated by Django 4.1.6 on 2023-02-10 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_remove_productname_language_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="companytype",
            name="type_name_en",
        ),
        migrations.RemoveField(
            model_name="companytype",
            name="type_name_sv",
        ),
        migrations.RemoveField(
            model_name="language",
            name="name_en",
        ),
        migrations.RemoveField(
            model_name="language",
            name="name_sv",
        ),
    ]
