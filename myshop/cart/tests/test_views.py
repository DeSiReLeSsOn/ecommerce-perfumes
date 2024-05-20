import pytest
from decimal import Decimal
from cart.forms import CartAddProductForm
from django.urls import reverse 
from shop.tests.conftest import *
from cart.cart import Cart






@pytest.mark.django_db
class TestViews:
    def test_cart_add_valid_data(self, client, test_product):
        url = reverse('cart:cart_add', kwargs={'product_id': test_product.id})
        data = {'quantity': 2, 'override': False}
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('cart:cart_detail')
        # Получаем экземпляр корзины для client
        cart = Cart(client)
        # Проверяем, что элемент в корзине для test_product содержит правильное количество и цену
        for item in cart:
            if item['product'] == test_product:
                assert item['quantity'] == 2
                assert item['price'] == Decimal(1300.00)
                break
        else:
            assert False, 'test_product not found in cart'