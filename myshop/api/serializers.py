from rest_framework import serializers
from shop.models import Product 
from django.contrib.auth.models import Group, User




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
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save() 
        return user

