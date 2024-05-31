import pytest 
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from shop.tests.conftest import test_user



@pytest.mark.django_db
class TestUserView:

    def test_register_user(self, client):

        endpoint = reverse('api:register')

        data_user = {
            'username': 'Greatest', 
            'email': 'pinkfloyd@gmail.com',
            'password': '12345678s'
        }


        response = client.post(endpoint, data_user)

        user = User.objects.get(username=data_user['username'])


        assert response.status_code == 201 
        assert user.username == data_user['username']
        assert user.email == data_user['email'] 

        user.delete()


    def test_get_user_token(self, client, test_user):
        
        endpoint = reverse('api:token_obtain_pair') 

        data_user = {
            'username': test_user.username, 
            'password': test_user.password
        }

        #client.force_authenticate(user=test_user)
        response = client.post(endpoint, data_user)


        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data








