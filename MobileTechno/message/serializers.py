# message/serializers.py
from rest_framework import serializers
from .models import User, Message

class UserSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل User.
    """
    class Meta:
        model = User
        fields = ['id', 'username']

class MessageSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل Message.
    """
    sender = UserSerializer(read_only=True)
    recipient = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        help_text="نام کاربری دریافت‌کننده پیام"
    )
    content = serializers.CharField(
        help_text="متن پیام"
    )

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp', 'is_read']
        read_only_fields = ['id', 'sender', 'timestamp', 'is_read']
