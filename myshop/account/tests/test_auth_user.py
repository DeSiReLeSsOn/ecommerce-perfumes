import pytest
from shop.tests.conftest import * 
from django.contrib.auth.models import User 
from django.urls import reverse 

@pytest.mark.django_db
class TestAuthUser:
    def test_auth(self, client, username=None, password=None):
        url = reverse('account:register')

        data = {'username': 'test_user',
                'email': 'test@gmail.com',
                'password1': 'test_password',
                'password2': 'test_password'}

        response = client.post(url, data)
        user = User.objects.get(email=data['email'])


        assert user.check_password(data['password1']) == True 


    def test_get_user(self, client, test_user):
        url = reverse('account:register')

        data = {'username': 'test_user',
                'email': 'test@gmail.com',
                'password1': 'test_password',
                'password2': 'test_password'}

        response = client.post(url, data)

        user = User.objects.get(pk=test_user.id)
        assert user is not None 


    def test_create_profile(self, client, test_user):
        user, created = User.objects.get_or_create(username='test_user1', password='12345678s', email='test1@gmail.com') 

        assert created == True
        assert user.username == 'test_user1' 
        assert user.email == 'test1@gmail.com'


