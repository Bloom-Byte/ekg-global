# Generated by Django 5.0.7 on 2024-07-25 11:52

import apps.portfolios.models
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stocks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('capital', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('description', models.TextField(blank=True, null=True)),
                ('brokerage_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolios', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Portfolio',
                'verbose_name_plural': 'Portfolios',
                'ordering': ['-created_at'],
                'unique_together': {('owner', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], max_length=120)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=12)),
                ('quantity', models.IntegerField()),
                ('date', models.DateField(validators=[apps.portfolios.models.validate_not_in_future])),
                ('brokerage_fee', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('commission', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('cdc', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('psx_laga', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('secp_laga', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('nccpl', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('cvt', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('wht', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('adv_tax', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('sst', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='stocks.stock')),
                ('portfolio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='portfolios.portfolio')),
            ],
            options={
                'verbose_name': 'Investment',
                'verbose_name_plural': 'Investments',
                'ordering': ['-added_at'],
            },
        ),
    ]
