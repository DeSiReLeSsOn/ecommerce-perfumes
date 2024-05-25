import pytest 
from shop.tests.conftest import * 
from orders.models import Order, OrderItem
from orders.views import * 
from orders.tasks import * 
from unittest.mock import patch





@patch('orders.tasks.send_mail')
@pytest.mark.django_db
def test_order_created_task(mock_send_mail, test_product, test_user):
    # Создаем новый заказ
    order = Order.objects.create(
        user=test_user,
        full_name='Ronaldo',
        email='test@gmail.com',
        address='Pogtugal',
        postal_code='123456',
        phone='+79595628159',
    )

    # Создаем тестовый OrderItem
    order_item = OrderItem.objects.create(
        order=order,
        product=test_product,
        price=test_product.price,
        quantity=1,
        user=test_user
    )

    # Вызываем задачу order_created
    order_created.delay(order.id)  

    # Проверяем, что email был отправлен с правильными данными
    mock_send_mail.assert_called_once_with(
        subject=f'Заказ № {order.id}',
        message=f'Дорогой {order.full_name},\n\n' \
                f'Вы успешно разместили заказ № {order.id}.\n' \
                f'Сумма заказа: {order.get_total_cost()}\n' \
                f'Товары в заказе:\n' \
                f'{order_item.product.name} - {order_item.quantity} шт., ' \
                f'{order_item.price} руб. за шт.\n',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.email]
    )

    # Проверяем, что задача вернула результат отправки email
    assert order_created.delay(order.id).get() is True 


