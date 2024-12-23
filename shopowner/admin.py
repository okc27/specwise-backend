from django.contrib import admin
from .models import Shop, ShopOwner

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'country', 'city', 'website_link', 'created_on')
    search_fields = ('shop_name', 'country', 'city')


@admin.register(ShopOwner)
class ShopOwnerAdmin(admin.ModelAdmin):
    # Access related fields from the Shop model
    list_display = ('get_full_name', 'email', 'phone_number', 'get_shop_name', 'get_country', 'get_city', 'registered_on')
    search_fields = ('first_name', 'last_name', 'email', 'shop__shop_name', 'shop__country', 'shop__city')

    # Define methods to retrieve related Shop fields
    @admin.display(ordering='shop__shop_name', description='Shop Name')
    def get_shop_name(self, obj):
        return obj.shop.shop_name if obj.shop else "N/A"

    @admin.display(ordering='shop__country', description='Country')
    def get_country(self, obj):
        return obj.shop.country if obj.shop else "N/A"

    @admin.display(ordering='shop__city', description='City')
    def get_city(self, obj):
        return obj.shop.city if obj.shop else "N/A"

    # Add method to display full name (first and last name)
    @admin.display(description='Full Name')
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
