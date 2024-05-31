from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from shop.models import Product 
from .serializers import ProductSerializer
from rest_framework import viewsets
from .serializers import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView 
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework_simplejwt.views import TokenBlacklistView



class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer





class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )


    def create_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'user': UserSerializer(user, context=self.get_serializer_context()).data}, status=status.HTTP_201_CREATED) 
    

class UserLoginView(TokenObtainPairView):
    pass