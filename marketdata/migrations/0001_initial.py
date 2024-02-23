# Generated by Django 4.2.7 on 2024-02-23 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BrokerSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('broker_name', models.CharField(max_length=255)),
                ('api_key', models.CharField(max_length=255)),
                ('api_secret', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MasterInstrumentList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('instrument_token', models.CharField(max_length=255)),
                ('exchange_token', models.CharField(max_length=255)),
                ('exchange', models.CharField(max_length=255)),
                ('trading_symbol', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('last_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ticket_size', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lot_size', models.CharField(max_length=255)),
                ('instrument_type', models.CharField(max_length=255)),
                ('segment', models.CharField(max_length=255)),
                ('broker_setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketdata.brokersetting')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalMarketDataSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateTimeField(auto_now_add=True)),
                ('to_date', models.DateTimeField(auto_now_add=True)),
                ('exchange', models.CharField(max_length=255)),
                ('stock_symbol', models.CharField(max_length=255)),
                ('resolution', models.CharField(max_length=255)),
                ('error_message', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField()),
                ('broker_setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketdata.brokersetting')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalDataFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('file_type', models.CharField(max_length=255)),
                ('file_path', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=255)),
                ('new_file_name', models.CharField(max_length=255)),
                ('broker_setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketdata.brokersetting')),
                ('historical_market_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketdata.historicalmarketdatasetting')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
