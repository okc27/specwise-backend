from django.db import models

class Shop(models.Model):
    shop_name = models.CharField(max_length=255, verbose_name="Shop Name")
    country = models.CharField(max_length=100, verbose_name="Country")
    city = models.CharField(max_length=100, verbose_name="City")
    website_link = models.URLField(max_length=500, verbose_name="Shop Website Link", default=None, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")

    def __str__(self):
        return f"{self.shop_name} ({self.city}, {self.country})"


class ShopOwner(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="First Name", default="DefaultFirstName")
    last_name = models.CharField(max_length=255, verbose_name="Last Name", default="DefaultLastName")
    email = models.EmailField(unique=True, verbose_name="Owner Email")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number" )
    username = models.CharField(max_length=255, unique=True, verbose_name="Username", default="default_user")
    password = models.CharField(max_length=255, verbose_name="Password", default="default_password")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="Shop", related_name="owners")
    registered_on = models.DateTimeField(auto_now_add=True, verbose_name="Registration Date")

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Owner of {self.shop.shop_name})"

