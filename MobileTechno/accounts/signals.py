# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserRequest, Profile, User

# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     """
#     ایجاد یا به‌روزرسانی پروفایل کاربر هنگام ایجاد یا به‌روزرسانی کاربر.
#     """
#     if created:
#         if Profile.objects.get(user=instance) is not None:
#             Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_request(sender, instance, created, **kwargs):
    """
    ایجاد یک UserRequest جدید هنگام ایجاد کاربر.
    """
    if created:
        UserRequest.objects.create(user=instance)
