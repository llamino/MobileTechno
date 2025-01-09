# accounts/models.py

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        if not phone_number:
            raise ValueError('Phone number is required')

        email = extra_fields.get('email', None)

        user = self.model(
            username=username,
            phone_number=phone_number,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"

class UserRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    requests_today = models.IntegerField(default=0)
    last_request = models.DateTimeField(default=timezone.now)

    def reset_requests_if_needed(self):
        if timezone.now().date() != self.last_request.date():
            self.requests_today = 0
            self.last_request = timezone.now()
            self.save()