# accounts/serializers.py
from rest_framework import serializers
from .models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'photo']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']


class RegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}, 'email': {'required': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        email = validated_data.get('email')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=password,
            email=email
        )
        Profile.objects.update_or_create(user=user, defaults=profile_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_or_email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super(CustomTokenObtainPairSerializer, self).__init__(*args, **kwargs)
        # حذف فیلد 'username'
        self.fields.pop('username', None)
        # افزودن فیلد 'username_or_email'
        self.fields['username_or_email'] = serializers.CharField()

    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')

        user = None

        # تلاش برای یافتن کاربر با نام کاربری
        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            pass

        # اگر کاربر پیدا نشد، تلاش برای یافتن با ایمیل
        if user is None:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                raise serializers.ValidationError("نام کاربری یا ایمیل و رمز عبور نامعتبر است.")

        # بررسی رمز عبور و فعال بودن کاربر
        if user and user.check_password(password):
            if not user.is_active:
                raise serializers.ValidationError("این حساب کاربری غیرفعال است.")

            refresh = self.get_token(user)

            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }

            return data
        else:
            raise serializers.ValidationError("نام کاربری یا ایمیل و رمز عبور نامعتبر است.")
