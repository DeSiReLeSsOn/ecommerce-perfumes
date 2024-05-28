import json
import pytest
from unittest.mock import patch, MagicMock
from django.http import HttpResponse
from payment.views import *
from shop.tests import conftest
from orders.models import Order, OrderItem 
from payment.tasks import payment_completed

@pytest.fixture
def mock_request(monkeypatch):
    """Создает мокированный запрос для тестирования"""
    mock_json_loads = MagicMock()
    monkeypatch.setattr('json.loads', mock_json_loads)
    request = MagicMock()
    request.body = json.dumps({'event': 'payment.succeeded', 'object': {'description': 'Заказ №123', 'id': 'some_payment_id'}})
    return request, mock_json_loads

def test_payment_succeeded(mock_request):
    """Проверяет обработку события payment.succeeded"""
    request, mock_json_loads = mock_request
    mock_json_loads.return_value = {'event': 'payment.succeeded', 
                                    'object': {'description': 'Заказ №123', 
                                              'id': 'some_payment_id', 
                                              'status': 'succeeded'}}  

 
    order_id = mock_json_loads.return_value['object']['description'].split('№')[1] 


    order = MagicMock(spec=Order, id=order_id, paid=False, save=MagicMock())

    with patch('payment.tasks.payment_completed.delay') as mock_payment_completed_delay:
        response = yookassa_webhook(request)


        order.paid = True


def test_payment_canceled(mock_request):

    request, mock_json_loads = mock_request
    mock_json_loads.return_value = {'event': 'payment.canceled', 'object': {'description': 'Заказ №123', 'id': 'some_payment_id'}}
    response = yookassa_webhook(request)
    assert response.status_code == 404

def test_invalid_event(mock_request):
    """Проверяет обработку некорректного события"""
    request, mock_json_loads = mock_request
    mock_json_loads.return_value = {'event': 'invalid_event', 'object': {'description': 'Заказ №123', 'id': 'some_payment_id'}}
    response = yookassa_webhook(request)
    assert response.status_code == 404

def test_key_error(mock_request):
    """Проверяет обработку KeyError"""
    request, mock_json_loads = mock_request
    mock_json_loads.return_value = None  
    response = yookassa_webhook(request)
    assert response.status_code == 500

def test_order_does_not_exist(mock_request):
    """Проверяет обработку Order.DoesNotExist"""
    request, mock_json_loads = mock_request
    mock_json_loads.return_value = {'event': 'payment.succeeded', 'object': {'description': 'Заказ №123', 'id': 'some_payment_id'}}  # Корректный JSON
    with patch('orders.views.get_object_or_404') as mock_get_object_or_404:
        mock_get_object_or_404.side_effect = Order.DoesNotExist
        response = yookassa_webhook(request)
        assert response.status_code == 400

def test_generic_exception(mock_request):
    """Проверяет обработку Exception"""
    request, mock_json_loads = mock_request
    mock_json_loads.return_value = {'event': 'payment.succeeded', 'object': {'description': 'Заказ №123', 'id': 'some_payment_id'}}  # Корректный JSON
    with patch('orders.views.get_object_or_404') as mock_get_object_or_404:
        mock_get_object_or_404.side_effect = Exception
        response = yookassa_webhook(request)
        assert response.status_code == 400

