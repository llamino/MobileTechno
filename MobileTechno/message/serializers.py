# message/serializers.py
from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    receiver = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp']