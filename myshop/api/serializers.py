from rest_framework import serializers
from shop.models import Product 



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        exclude = ('slug', 'image', 'updated', 'search_count', 'views_count',)