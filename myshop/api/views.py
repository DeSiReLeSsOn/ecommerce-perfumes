from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from shop.models import Product 
from .serializers import ProductSerializer
from rest_framework import viewsets


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
