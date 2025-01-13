# mobile/serializers.py
from rest_framework import serializers
from .models import Mobile

class MobileListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Mobile objects with limited fields.
    """

    class Meta:
        model = Mobile
        fields = ['product_id', 'name', 'price', 'image_url']


class MobileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed Mobile view with all fields.
    """

    class Meta:
        model = Mobile
        fields = '__all__'
