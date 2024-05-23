import pytest 
from shop.tests.conftest import * 
from django.urls import reverse
from cart.cart import Cart 
from orders.forms import OrderCreateForm


@pytest.mark.django_db
class TestOrderViews:
    def test_order_create(self, client, test_order, test_user, test_coupon):
        client.force_login(test_user)
        data = {'full_name': test_order.full_name,
            'email': test_order.email,
            'address': test_order.address,
            'postal_code': test_order.postal_code,
            'phone': test_order.phone}
        
        url = reverse('orders:order_create')

        response = client.post(url, data)

        
        assert response.status_code == 302
        assert response.url == reverse('payment:process')


        order = Order.objects.last()
        assert order.full_name == 'Ronaldo'
        assert order.email == 'test@gmail.com' 
        assert order.address == 'Pogtugal' 
        assert order.postal_code == '123456' 
        assert order.phone == '+79595628159'   

        url = reverse('payment:process')
        response = client.get(url)


        assert response.status_code == 200 
        assert response.templates[0].name == 'payment/process.html'

    def test_create_order_with_coupon(self, client, test_order_with_coupon, test_coupon):
        data = {'full_name': test_order_with_coupon.full_name,
            'email': test_order_with_coupon.email,
            'address': test_order_with_coupon.address,
            'postal_code': test_order_with_coupon.postal_code,
            'phone': test_order_with_coupon.phone,
            'coupon': test_order_with_coupon.coupon}
        url = reverse('orders:order_create') 
        response = client.post(url, data) 


        order = Order.objects.last()
        assert order.coupon == test_coupon


    def test_order_contains_form(self, client):
        cart = Cart(client) 

        url = reverse('orders:order_create')
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.templates[0].name == 'orders/order/create.html'
        assert 'cart' in response.context
        assert 'form' in response.context  

    def test_get_user_orders(self, client, test_user, test_order):

        client.force_login(test_user)  
        url = reverse('orders:get_user_orders')
        response = client.get(url)
        assert response.status_code == 200  


        orders = response.context['orders']
        assert orders.count() == 1
        assert orders[0] == test_order
        assert response.templates[0].name == 'orders/order/order_list.html'


        order_items = response.context['order_items']
        assert order_items.count() == test_order.items.count() 


    def test_get_user_orders_unauthorized(self, client):

        url = reverse('orders:get_user_orders')
        response = client.get(url)
        assert response.status_code == 302  
        assert response.url == f'/accounts/login/?next={url}'





    





