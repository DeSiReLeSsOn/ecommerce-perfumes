import pytest
from shop.tests.conftest import * 
from django.contrib.auth.models import User 
from django.urls import reverse
from account.forms import UserCreateForm, UserUpdateForm



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


    def test_correct_data_user_login(self, client, test_user):
        url = reverse('account:login')

        data = {'username': test_user.username,
                'password': 'test_password'} 
        
        response = client.post(url, data) 

        user = User.objects.get(username=test_user.username)
        assert response.status_code == 302
        assert response.url == reverse('account:dashboard')
        #assert user.is_authenticated == True 
        response = client.get(reverse('account:dashboard')) 
        assert response.context['user'].is_authenticated == True
 




    def test_invalid_data_user_login(self, client, test_user):
        url = reverse('account:login')
        

        data = {'username': test_user.username, 
                'password': 'wrong_password'}

        response = client.post(url, data) 


        assert response.status_code == 302
        assert response.url == reverse('account:login') 
        response = client.get(url) 
        assert response.context['user'].is_authenticated == False 



    def test_logout_user(self, client, test_user):
        client.force_login(test_user)


        url = reverse('account:logout') 

        response = client.get(url) 


        assert client.session.get('_auth_user_id') is None
        assert client.session.get('_auth_user_hash') is None


        assert response.status_code == 302
        assert response.url == reverse('shop:product_list') 


    def test_dashboard_user(self, client, test_user):
        client.force_login(test_user) 

        url = reverse('account:dashboard') 

        response = client.get(url) 


        assert response.status_code == 200 
        assert response.templates[0].name == 'account/dashboard/dashboard.html' 


    def test_profile_user(self, client, test_user):
        client.force_login(test_user) 

        url = reverse('account:profile-management') 

        response = client.get(url) 
        assert response.status_code == 200 
        assert response.templates[0].name == 'account/dashboard/profile-management.html'
        assert 'form' in response.context 
        form = response.context['form'] 
        assert isinstance(form, UserUpdateForm)


    def test_delete_user(self, client, test_user):
        client.force_login(test_user) 


        url = reverse('account:delete-user') 
        response = client.get(url) 

        assert response.status_code == 200
        assert response.templates[0].name == 'account/dashboard/account-delete.html' 


        response = client.post(url) 
        assert response.status_code == 302
        assert response.url == reverse('shop:product_list') 









        
        