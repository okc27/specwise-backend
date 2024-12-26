from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from rest_framework import status
from .serializers import ProductSerializer

class RandomProductsByCategoryAPIView(APIView):
    def get(self, request):
        # Get distinct categories excluding 'Supplies' and excluding products from shop_id 1
        products = Product.objects.exclude(store_id=1).exclude(category="Supplies").values('category').distinct()
        random_products = []

        for product in products:
            # Fetch random products per category, excluding products from shop_id 1 and 'Supplies' category
            category_products = Product.objects.filter(category=product['category']).exclude(store_id=1).exclude(category="Supplies").order_by('?')[:2]
            random_products.extend(category_products.values())

        return Response(random_products, status=status.HTTP_200_OK)


class AddProductAPIView(APIView):
    def post(self, request):
        # Set default values for 'rating' and 'link' if not provided
        data = request.data
        if 'rating' not in data:
            data['rating'] = None
        if 'link' not in data:
            data['link'] = None
        
        # Serialize the data and save the product
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)