from celery import shared_task
from django.core.mail import send_mail
from .models import Order 
from myshop import settings






@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Заказ № {order.id}'
    message = f'Дорогой {order.full_name},\n\n' \
              f'Вы успешно разместили заказ № {order.id}.\n' \
              f'Сумма заказа: {order.get_total_cost()}\n' \
              f'Товары в заказе:\n'

    for item in order.items.all():
        message += f'{item.product.name} - {item.quantity} шт., ' \
                  f'{item.price} руб. за шт.\n'

    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
    return mail_sent









