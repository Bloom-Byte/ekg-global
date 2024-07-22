# Generated by Django 5.0.7 on 2024-07-19 15:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="KSE",
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
                ("date", models.DateField()),
                ("open", models.FloatField()),
                ("high", models.FloatField()),
                ("low", models.FloatField()),
                ("close", models.FloatField()),
                ("volume", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Rate",
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
                ("ticker", models.CharField(max_length=120)),
                ("mkt", models.CharField(max_length=120)),
                ("previous_close", models.FloatField()),
                ("open", models.FloatField()),
                ("high", models.FloatField()),
                ("low", models.FloatField()),
                ("close", models.FloatField()),
                ("change", models.FloatField()),
                ("volume", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Ticker",
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
                ("name", models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name="Portfolio",
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
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Trade",
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
                    "transaction_type",
                    models.CharField(
                        choices=[("buy", "buy"), ("sell", "sell")], max_length=120
                    ),
                ),
                ("symbol", models.CharField(max_length=120, null=True)),
                ("date", models.DateField()),
                ("price", models.IntegerField()),
                ("quantity", models.IntegerField()),
                (
                    "portfolio",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pfolio",
                        to="app.portfolio",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
