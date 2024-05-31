from rest_framework import serializers
from shop.models import Product 
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        exclude = ('slug', 'image', 'updated', 'search_count', 'views_count',) 




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('username', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
