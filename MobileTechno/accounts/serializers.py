# accounts/serializers.py
from rest_framework import serializers
from .models import User, Profile
from django.contrib.auth import authenticate
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
        fields = ['id', 'username', 'phone_number', 'profile']


class RegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'password', 'profile', 'email']
        extra_kwargs = {'password': {'write_only': True}, 'email': {'required': False, 'allow_blank': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        email = validated_data.get('email', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            password=password,
            email=email
        )
        Profile.objects.update_or_create(user=user, **profile_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    username_or_phone = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super(CustomTokenObtainPairSerializer, self).__init__(*args, **kwargs)
        # حذف فیلد 'username'
        self.fields.pop('username', None)
        # افزودن فیلد 'username_or_phone'
        self.fields['username_or_phone'] = serializers.CharField()

    def validate(self, attrs):

        username_or_phone = attrs.get('username_or_phone')
        password = attrs.get('password')

        user = None

        # تلاش برای یافتن کاربر با نام کاربری
        try:
            user = User.objects.get(username=username_or_phone)
        except User.DoesNotExist:
            pass

        # اگر کاربر پیدا نشد، تلاش برای یافتن با شماره تلفن
        if user is None:
            try:
                user = User.objects.get(phone_number=username_or_phone)
            except User.DoesNotExist:
                raise serializers.ValidationError("نام کاربری یا شماره تلفن و رمز عبور نامعتبر است.")

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
                    'phone_number': user.phone_number,
                    'email': user.email,
                }
            }

            return data
        else:
            raise serializers.ValidationError("نام کاربری یا شماره تلفن و رمز عبور نامعتبر است.")







