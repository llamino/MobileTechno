# acccounts/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class UsernameOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        username_or_phone = username or kwargs.get('username_or_phone')
        if username_or_phone is None or password is None:
            return None
        try:
            user = User.objects.get(username=username_or_phone)
        except User.DoesNotExist:
            try:
                user = User.objects.get(phone_number=username_or_phone)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        return None