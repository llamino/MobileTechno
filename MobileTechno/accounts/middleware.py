# accounts/middleware.py
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.backends import TokenBackend
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()

class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    میان‌افزار برای احراز هویت کاربران با استفاده از توکن‌های JWT ذخیره‌شده در کوکی‌ها.
    """
    def process_request(self, request):
        token = request.COOKIES.get('access_token')

        if token:
            try:
                token_backend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
                valid_data = token_backend.decode(token, verify=True)
                user_id = valid_data.get('user_id')

                user = User.objects.get(id=user_id)
                request.user = user
            except Exception as e:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
