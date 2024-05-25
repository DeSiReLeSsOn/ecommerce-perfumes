import pytest
from decimal import Decimal
from yookassa import Payment , Configuration , Webhook
from django.urls import reverse 
from shop.tests.conftest import *
from orders.models import Order, OrderItem
from coupons.forms import CouponApplyForm
import json 
from django.http.response import JsonResponse 
from payment.views import * 
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import get_object_or_404 








@pytest.mark.django_db
def test_payment_process_redirects(test_order, client, test_order_item):
    """Проверяет, что функция payment_process создает платеж в YooMoney с использованием реального API и перенаправляет на страницу оплаты."""

    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


    session = client.session
    session['order_id'] = test_order_item.order.id
    session.save()


    payment = Payment.create({
        "amount": {
            "value": Decimal(test_order.get_total_cost()),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": reverse('payment:completed'),
        },
        "capture": True,
        "description": "Оплата за заказ {}".format(test_order.id),
    })


    url = reverse('payment:process')
    response = client.post(url)


    assert response.status_code == 302
    assert payment.status == 'pending'
    assert payment.amount.value == Decimal(test_order.get_total_cost())
    assert payment.amount.currency == 'RUB'
    assert payment.description == f"Оплата за заказ {test_order.id}"


@pytest.mark.django_db
def test_payment_process_get_correct_template(test_order, client, test_order_item):

    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


    session = client.session
    session['order_id'] = test_order_item.order.id
    session.save()

    url = reverse('payment:process')
    response = client.get(url)


    assert response.status_code == 200

 
    assert response.templates[0].name == 'payment/process.html'

 
    assert 'order' in response.context
    assert response.context['order'] == test_order



