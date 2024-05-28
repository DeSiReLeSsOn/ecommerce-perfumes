import pytest
from shop.tests.conftest import * 
from django.contrib.auth.models import User 
from django.urls import reverse 

@pytest.mark.django_db
class TestAuthUser:
    def test_auth(self, client, test_user, username=None, password=None):
        url = reverse('account:register')

        data = {'username': 'test_user',
                'email': 'test@gmail.com',
                'password1': 'test_password',
                'password2': 'test_password'}

        response = client.post(url, data)
        user = User.objects.get(email=data['email'])


        assert user.check_password(data['password1']) == True 


