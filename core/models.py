from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings
import ast


SECRET_KEY = b'g6stRwKJ9xVVWhmUh8p8AuyCJdPS8XrTXqfcYG9DEOQ='


def encrypt_data(data, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
        cipher = Fernet(key)
        encrypted_data = ast.literal_eval(encrypted_data) 
        decrypted_data = cipher.decrypt(encrypted_data).decode()
        return decrypted_data

class BrokerSettings(models.Model):
    # Your fields here
    broker_name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.broker_name

class MasterInstrumentLists(models.Model):
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
    broker_setting = models.ForeignKey(BrokerSettings, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class HistoricalDataFiles(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    new_file_name = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    broker_setting = models.ForeignKey('BrokerSettings', on_delete=models.CASCADE)
    historical_market_data = models.ForeignKey('HistoricalMarketDataSettings', on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name
class HistoricalMarketDataSettings(models.Model):
    from_date = models.DateTimeField(auto_now_add=True)
    to_date = models.DateTimeField(auto_now_add=True)
    exchange = models.CharField(max_length=255)
    stock_symbol = models.CharField(max_length=255)
    resolution = models.CharField(max_length=255)
    error_message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    broker_setting = models.ForeignKey('BrokerSettings', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.stock_symbol} - {self.resolution}'

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=255, null=True, blank=True)

    def get_decrypted_key(self, broker_name):
        #if broker_name == 'Zerodha':
            #field = self.zerodha_key
        #elif broker_name == 'ICICI':
            #field = self.icici_key
        return decrypt_data(field, SECRET_KEY)

    def save(self, *args, **kwargs):
        #if self.zerodha_key:
            #self.zerodha_key = encrypt_data(self.zerodha_key, SECRET_KEY)
        #if self.icici_key:
            #self.icici_key = encrypt_data(self.icici_key, SECRET_KEY)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email


    