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
    print(f'Request body: {request.body}')
    event_json = json.loads(request.body)
    print(f'Event json: {event_json}')
    try:
        if event_json['event'] == "payment.succeeded":
            payment_object = event_json['object']
            print(f'Payment object: {payment_object}')
            order_id = int(payment_object['description'].split()[-1])
            print(f'Order id: {order_id}')
            order = get_object_or_404(Order, id=order_id)
            print(f'Order before update: {order}')
            order.paid = True
            order.save()
            print(f'Order after update: {order}')
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)

    except KeyError:
        print('KeyError')
        return HttpResponse(status=400)

    except Order.DoesNotExist:
        print('Order.DoesNotExist')
        return HttpResponse(status=400)

    except Exception as e:
        print(f'Exception: {e}')
        return HttpResponse(status=400)

    return HttpResponse(status=405)







def payment_completed(request):
    return render(request, 'payment/completed.html')



def payment_canceled(request):
    return render(request, 'payment/canceled.html') 











