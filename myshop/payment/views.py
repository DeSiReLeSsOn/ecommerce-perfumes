from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from orders.models import Order, OrderItem
from yookassa import Payment , Configuration , Webhook
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart
from shop.models import Product
#import stripe
import uuid
from coupons.models import Coupon
import json
from django.http import HttpResponse
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory, WebhookNotification
from .tasks import payment_completed

#stripe
#stripe.api_key = settings.STRIPE_SECRET_KEY
#stripe.api_version = settings.STRIPE_API_VERSION











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
                "value": Decimal(order.get_total_cost()),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": success_url,
            },
            "capture": True,
            "description": "Оплата за заказ {}".format(order.id),
        })

        return redirect(payment.confirmation.confirmation_url, code=303)
    else:
        return render(request, 'payment/process.html', locals())




@csrf_exempt
def yookassa_webhook(request):
    #if request.method == 'POST':
    event_json = json.loads(request.body)
    try:
        if event_json['event'] == "payment.succeeded":
            payment_object = event_json['object']
            order_id = int(event_json['object']['description'].split()[-1])
            order = get_object_or_404(Order, id=order_id)
            order.paid = True
            order.save() 
            payment_completed.delay(order.id)
                
            return HttpResponse(status=200)
        else:
                # Другие типы событий обработайте по необходимости
            return HttpResponse(status=404)
        
    except KeyError:
            # Обработка ошибок, если ключи отсутствуют в JSON или другие проблемы с данными
        return HttpResponse(status=400)
        
    except Order.DoesNotExist:
            # Обработка ошибок, если заказ с указанным ID не найден
        return HttpResponse(status=400)
        
    except Exception as e:
            # Обработка других исключений, если они возникнут
        return HttpResponse(status=400)

    return HttpResponse(status=405)


def payment_completed(request):
    return render(request, 'payment/completed.html')



def payment_canceled(request):
    return render(request, 'payment/canceled.html') 











