from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings
import ast


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.user.email


SECRET_KEY = b'g6stRwKJ9xVVWhmUh8p8AuyCJdPS8XrTXqfcYG9DEOQ='


def encrypt_data(data, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

class BrokerSetting(models.Model):
    broker_name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.broker_name

    def save(self, *args, **kwargs):
        # Encrypt the field before saving
        self.api_key = encrypt_data(self.api_key, SECRET_KEY)
        self.api_secret = encrypt_data(self.api_secret, SECRET_KEY)
        super().save(*args, **kwargs)
    def decrypt_data(encrypted_data, key):
        cipher = Fernet(key)
        encrypted_data = ast.literal_eval(encrypted_data) 
        decrypted_data = cipher.decrypt(encrypted_data).decode()
        return decrypted_data
    