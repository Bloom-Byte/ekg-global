# Generated by Django 5.1 on 2024-09-04 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_stock_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='is_kse100',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stock',
            name='is_kse30',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stock',
            name='is_kse50',
            field=models.BooleanField(default=False),
        ),
    ]