# Generated by Django 4.1.3 on 2023-01-31 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("shared", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ChangeType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("change_type", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "activation_date",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                (
                    "external_website_url",
                    models.CharField(blank=True, default=None, max_length=1000, null=True),
                ),
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="company_profile_picture",
                    ),
                ),
            ],
            options={
                "verbose_name": "company",
                "verbose_name_plural": "companies",
            },
        ),
        migrations.CreateModel(
            name="CompanyRole",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("role_name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="CompanyStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status_name", models.CharField(max_length=50, unique=True)),
                ("description", models.CharField(max_length=200)),
            ],
            options={
                "verbose_name": "Company Status",
                "verbose_name_plural": "Company Statuses",
            },
        ),
        migrations.CreateModel(
            name="CompanyType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type_name", models.CharField(max_length=50, unique=True)),
                (
                    "type_name_sv",
                    models.CharField(max_length=50, null=True, unique=True),
                ),
                (
                    "type_name_en",
                    models.CharField(max_length=50, null=True, unique=True),
                ),
                ("description", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="ContactType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("contact_type", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("currency_code", models.CharField(max_length=3, unique=True)),
            ],
            options={
                "verbose_name_plural": "Currencies",
            },
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("iso_639_1", models.CharField(max_length=2, unique=True)),
                ("name", models.CharField(max_length=50)),
                ("name_sv", models.CharField(max_length=50, null=True)),
                ("name_en", models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_code", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProductName",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "language",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="main.language"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="name_translations",
                        to="main.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "price_per_unit",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
                ),
                ("unit_type", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "order_type",
                    models.CharField(
                        choices=[("sell", "Sell order"), ("buy", "Buy order")],
                        max_length=10,
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="main.company"),
                ),
                (
                    "currency",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="main.currency"),
                ),
                (
                    "product",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="main.product"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(max_length=500)),
                (
                    "description",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contacts",
                        to="main.company",
                    ),
                ),
                (
                    "contact_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="main.contacttype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CompanyUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users",
                        to="main.company",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="main.companyrole",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="companies",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CompanyDescription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.CharField(max_length=2000)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="descriptions",
                        to="main.company",
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
        migrations.CreateModel(
            name="CompanyChange",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("field", models.CharField(max_length=50)),
                ("changed", models.DateTimeField(auto_now_add=True)),
                ("new_value", models.TextField()),
                (
                    "change_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="main.changetype",
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="main.company"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="company",
            name="company_types",
            field=models.ManyToManyField(blank=True, related_name="companies", to="main.companytype"),
        ),
        migrations.AddField(
            model_name="company",
            name="content_languages",
            field=models.ManyToManyField(blank=True, related_name="companies", to="main.language"),
        ),
        migrations.AddField(
            model_name="company",
            name="status",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="main.companystatus"),
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "address_type",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("addressee", models.CharField(blank=True, max_length=100, null=True)),
                ("co_address", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "street_address",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("city", models.CharField(blank=True, max_length=20, null=True)),
                ("zip_code", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="addresses",
                        to="main.company",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="shared.country",
                    ),
                ),
            ],
            options={
                "verbose_name": "Address",
                "verbose_name_plural": "Addresses",
            },
        ),
    ]
