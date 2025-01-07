# accounts/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserRequest

@receiver(post_save, sender=User)
def create_user_request(sender, instance, created, **kwargs):
    if created:
        UserRequest.objects.create(user=instance)