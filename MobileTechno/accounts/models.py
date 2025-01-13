# accounts/models.py
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class UserRequest(models.Model):
    """
    Model to track the number of requests a user has made in a day.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    requests_today = models.IntegerField(default=0)
    last_request = models.DateTimeField(default=timezone.now)

    def reset_requests_if_needed(self):
        """
        Reset the request count if a new day has started.
        """
        if timezone.now().date() != self.last_request.date():
            self.requests_today = 0
            self.last_request = timezone.now()
            self.save()

    def __str__(self):
        return f"{self.user.username} - {self.requests_today} requests today"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"


# اگر UserRequest دیگر مورد نیاز نیست، می‌توان آن را حذف کرد.
# اما اگر همچنان نیاز دارید، اطمینان حاصل کنید که به User بدون phone_number مرتبط باشد.

