from decimal import Decimal
import yookassa
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponseRedirect, HttpResponse
from orders.models import Order, OrderItem
from yookassa import Payment , Configuration , Webhook
from yookassa.domain.notification import WebhookNotification
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart
from shop.models import Product
import stripe
import uuid
from django.http import JsonResponse
import requests
from coupons.models import Coupon
import json

#stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION





"""def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
                        reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(
                        reverse('payment:canceled'))

        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            }) 

        if order.coupon:
            stripe_coupon = stripe.Coupon.create(name=order.coupon.code, percent_off=order.discount, duration='once')
            session_data['discounts'] = [{
                'coupon': stripe_coupon.id 
        }]

        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)

    else:
        return render(request, 'payment/process.html', locals())"""
    




#def payment_completed(request):
#    return render(request, 'payment/completed.html')


#def payment_canceled(request):
#    return render(request, 'payment/canceled.html')
    







"""def payment_process(request):
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
                        reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(
                        reverse('payment:canceled'))
        for item in order.items.all():
            payment = Payment.create({
                "amount": {
                    "value": int(item.price),
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": success_url
                },
                "capture": True,
                "test": True,
                "description": "Payment for order {}".format(order.id)
            })
        return redirect(payment.confirmation.confirmation_url, code=303)
    else:
        return render(request, 'payment/process.html', locals())"""


"""def payment_process(request):
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
                        reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(
                        reverse('payment:canceled'))
        payment = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        for item in order.items.all():
            payment['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'RUB',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
                "capture": True,
                "test": True,
                "confirmation": {
                    "type": "redirect",
                    "return_url": success_url
                },
            }) 
        if order.coupon:
            # Replace this with the appropriate code to create a yookassa discount
            payment['discounts'] = [{
                'coupon': order.coupon.code 
        }]
        session = Payment.create(payment['line_items'])
        return redirect(session.confirmation.confirmation_url, code=303)
    else:
        return render(request, 'payment/process.html', locals())"""




def payment_process(request):
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        payment = Payment.create({
            "amount": {
                "value": float(order.get_total_cost()),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": success_url
            },
            "capture": True,
            "test": True,
            "description": "Оплата за заказ {}".format(order.id),
        })

        return redirect(payment.confirmation.confirmation_url, code=303)
    else:
        return render(request, 'payment/process.html', locals())


    

def payment_completed(request):
    return render(request, 'payment/completed.html')



def payment_canceled(request):
    return render(request, 'payment/canceled.html') 


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip 


@csrf_exempt
def yookassa_webhook(request):
    webhook = Webhook(request.body, request.headers['Content-Type'])
    event = webhook.parse()
    
    # Обработка события оплаты
    if event.type == 'payment.succeeded':
        
        return HttpResponse(status=200)
    
    return HttpResponse(status=200) 
    
    #2Второй вариант
    ip = get_client_ip(request)  # Получите IP запроса
    if not SecurityHelper().is_ip_trusted(ip):
        return HttpResponse(status=400)

    # Извлечение JSON объекта из тела запроса
    event_json = json.loads(request.body)
    try:
        # Создание объекта класса уведомлений в зависимости от события
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            # Специфичная логика
            # ...

        elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
        else:
            # Обработка ошибок
            return HttpResponse(status=400)  # Сообщаем кассе об ошибке

        Configuration.configure('XXXXXX', 'test_XXXXXXXX')
        # Получим актуальную информацию о платеже
        payment_info = Payment.find_one(some_data['paymentId'])
        if payment_info:
            payment_status = payment_info.status
            # Специфичная логика
            # ...
        else:
            # Обработка ошибок
            return HttpResponse(status=400)  # Сообщаем кассе об ошибке

    except Exception:
        # Обработка ошибок
        return HttpResponse(status=400)  # Сообщаем кассе об ошибке

    return HttpResponse(status=200) 








"""def webhook_view(request):
    webhook = Webhook(request.body, request.headers['Content-Type'])
    event = webhook.parse()

    # Обработка события оплаты
    if event.type == 'payment.succeeded':
        # Обновите статус заказа или выполните другие необходимые действия
        return HttpResponse(status=200)

    return HttpResponse(status=200)"""