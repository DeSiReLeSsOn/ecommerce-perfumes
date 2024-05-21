import pytest
from decimal import Decimal
from cart.forms import CartAddProductForm
from django.urls import reverse 
from shop.tests.conftest import *
from cart.cart import Cart
from coupons.forms import CouponApplyForm





@pytest.mark.django_db
class TestViews:
    def test_cart_add(self, client, test_product):
        url = reverse('cart:cart_add', kwargs={'product_id': test_product.id})
        data = {'quantity': 2, 'override': False}
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('cart:cart_detail')
        cart = Cart(client)

        for item in cart:
            if item['product'] == test_product:
                assert item['quantity'] == 2
                assert item['price'] == Decimal(1300.00)
                break
        else:
            assert False, 'test_product not found in cart' 

    def test_cart_remove_item(self, client, test_product):
        url = reverse('cart:cart_remove', kwargs={'product_id': test_product.id})
        response = client.post(url) 
        cart = Cart(client) 
        assert response.status_code == 302 

        url = reverse('cart:cart_detail')
        response = client.get(url)
        assert len(response.context['cart']) == 0  


    def test_cart_detail(self, client):
        url = reverse('cart:cart_detail')
        response = client.get(url) 


        assert response.context['coupon_apply_form'] is not None
        assert response.context['recommended_products'] is not None
        assert len(response.context['recommended_products']) == 0

        