# hardware_data/models.py
from django.db import models

# models.py
class Product(models.Model):
    store_id = models.IntegerField()
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    link = models.URLField(blank=True, null=True, default=None)  # Ensure link is optional with default=None

    def __str__(self):
        return self.name
