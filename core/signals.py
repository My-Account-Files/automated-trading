from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_userdetails(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(user=instance)