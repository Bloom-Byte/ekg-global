# Generated by Django 5.1 on 2024-09-24 19:01

import timezone_field.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default='UTC'),
        ),
    ]
