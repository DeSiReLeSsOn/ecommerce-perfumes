import pytest
from shop.tests.conftest import * 
from django.contrib.auth.models import User 
from django.urls import reverse
from account.forms import UserCreateForm


@pytest.mark.django_db
class TestAuth:
    def test_register(self, client):
        url = reverse('account:register')

        data = {'username': 'test_user',
                'email': 'test@gmail.com',
                'password1': 'test_password',
                'password2': 'test_password'}

        response = client.post(url, data)

        assert response.status_code == 302
        user = User.objects.get(username='test_user')
        assert user.username == 'test_user'
        assert user.email == 'test@gmail.com'
        assert user.is_active == False 


        url = reverse('account:register') 

        response = client.get(url) 

         

        assert response.status_code == 200 
        assert 'form' in response.context
        form = response.context['form']
        assert isinstance(form, UserCreateForm)
        assert 'account/registration/register.html' in [
            template.name for template in response.templates
        ]
