# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserRequest, Profile, User
# accounts/signals.py

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    ایجاد پروفایل برای کاربر جدید یا به‌روزرسانی پروفایل برای کاربر موجود.
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
@receiver(post_save, sender=User)
def create_user_request(sender, instance, created, **kwargs):
    if created:
        UserRequest.objects.create(user=instance)

