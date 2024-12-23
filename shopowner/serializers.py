from rest_framework import serializers
from .models import Shop, ShopOwner

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'shop_name', 'country', 'city', 'website_link', 'created_on']
        read_only_fields = ['created_on']

class ShopOwnerSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()  # Nested serializer for shop details

    class Meta:
        model = ShopOwner
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'username', 'password', 'shop', 'registered_on']
        read_only_fields = ['registered_on']

    def create(self, validated_data):
        shop_data = validated_data.pop('shop')
        shop, _ = Shop.objects.get_or_create(**shop_data)
        owner = ShopOwner.objects.create(shop=shop, **validated_data)
        return owner
