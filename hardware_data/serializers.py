# serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'rating': {'required': False},  # Make rating optional
            'link': {'required': False}     # Make link optional
        }
