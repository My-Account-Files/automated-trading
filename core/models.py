from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
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

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=255, null=True, blank=True)
    zerodha_key = models.CharField(max_length=255, null=True, blank=True)
    icici_key = models.CharField(max_length=255, null=True, blank=True)


    def get_decrypted_key(self, broker_name):
        if broker_name == 'Zerodha':
            field = self.zerodha_key
        elif broker_name == 'ICICI':
            field = self.icici_key
        return decrypt_data(field, SECRET_KEY)

    def save(self, *args, **kwargs):
        if self.zerodha_key:
            self.zerodha_key = encrypt_data(self.zerodha_key, SECRET_KEY)
        if self.icici_key:
            self.icici_key = encrypt_data(self.icici_key, SECRET_KEY)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email
    
