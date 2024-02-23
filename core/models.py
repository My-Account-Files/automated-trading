from django.db import models
from django.contrib.auth.models import User


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.user.email


    