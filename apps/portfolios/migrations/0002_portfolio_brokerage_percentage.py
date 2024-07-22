# Generated by Django 5.0.7 on 2024-07-21 17:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portfolios", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfolio",
            name="brokerage_percentage",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=2, null=True
            ),
        ),
    ]
