from django.urls import path
from .views import RandomProductsByCategoryAPIView, AddProductAPIView

urlpatterns = [
    path('random-products-by-category/', RandomProductsByCategoryAPIView.as_view(), name='random-products-by-category'),
    path('add-product/', AddProductAPIView.as_view(), name='add-product'),
]
