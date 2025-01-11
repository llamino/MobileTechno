# acccounts/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class UsernameOrEmailBackend(ModelBackend):
    """
    بک‌اند سفارشی برای احراز هویت با استفاده از نام کاربری یا ایمیل.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        username_or_email = username or kwargs.get('username_or_email')
        if username_or_email is None or password is None:
            return None
        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        return None