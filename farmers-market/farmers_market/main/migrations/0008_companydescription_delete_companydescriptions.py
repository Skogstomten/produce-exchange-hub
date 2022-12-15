# Generated by Django 4.1.3 on 2022-12-05 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_country_name_alter_country_country_iso_3166_1"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompanyDescription",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", models.CharField(max_length=2000)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="descriptions", to="main.company"
                    ),
                ),
                (
                    "language",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="company_descriptions",
                        to="main.language",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="CompanyDescriptions",
        ),
    ]
