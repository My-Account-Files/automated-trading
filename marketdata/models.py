from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings
import ast
from core.models import *


class MasterInstrumentList(models.Model):
    broker_setting = models.ForeignKey(BrokerSetting, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    instrument_token = models.CharField(max_length=255)
    exchange_token = models.CharField(max_length=255)
    exchange = models.CharField(max_length=255)
    trading_symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    last_price = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_size = models.DecimalField(max_digits=10, decimal_places=2)
    lot_size = models.CharField(max_length=255)
    instrument_type = models.CharField(max_length=255)
    segment = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class HistoricalMarketDataSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    broker_setting = models.ForeignKey(BrokerSetting, on_delete=models.CASCADE)
    from_date = models.DateTimeField(auto_now_add=True)
    to_date = models.DateTimeField(auto_now_add=True)
    exchange = models.CharField(max_length=255)
    stock_symbol = models.CharField(max_length=255)
    resolution = models.CharField(max_length=255)
    error_message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return f'{self.stock_symbol} - {self.resolution}'


class HistoricalDataFile(models.Model):
    broker_setting = models.ForeignKey(BrokerSetting, on_delete=models.CASCADE)
    historical_market_data = models.ForeignKey(HistoricalMarketDataSetting, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    new_file_name = models.CharField(max_length=255)

    def __str__(self):
        return self.file_name
