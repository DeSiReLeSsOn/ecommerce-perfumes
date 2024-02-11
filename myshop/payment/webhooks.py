import json
from django.http import HttpResponse
from yookassa import Configuration, Payment, Webhook
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory
from yookassa.domain.common import SecurityHelper
from django.views.decorators.csrf import csrf_exempt
#from .tasks import payment_completed
from orders.models import Order
from myshop import settings 
from django.shortcuts import render, redirect, reverse, get_object_or_404



"""@csrf_exempt
def yookassa_webhook(request, order_id):
    order = Order.objects.get(id=order_id)
    payload = request.body
    sig_header = request.META['HTTP_YOOKASSA_SIGNATURE']
    event = None

    try:
        event = Webhook.construct_event(
                    payload,
                    sig_header,
                    settings.YOOKASSA_WEBHOOK_SECRET)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except Webhook.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
        # пометить заказ как оплаченный
            order.paid = True
            order.save()
    return HttpResponse(status=200)

            # save items bought for product recommendations
            #product_ids = order.items.values_list('product_id')
            #products = Product.objects.filter(id__in=product_ids)
            #r = Recommender()
            #r.products_bought(products)
            
            # launch asynchronous task
            #payment_completed.delay(order.id)"""


@csrf_exempt
def yookassa_webhook(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    # Если хотите убедиться, что запрос пришел от ЮКасса, добавьте проверку:
    if request.method == 'POST':
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
                    # пометить заказ как оплаченный
                order.paid = True
                order.save()    
            

            elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
                some_data = {
                    'paymentId': response_object.id,
                    'paymentStatus': response_object.status,
            }
                order.paid = False
                order.save()
            

            else:
                # Обработка ошибок
                return HttpResponse(status=400)  # Сообщаем кассе об ошибке
            
            Configuration.configure('XXXXXX', 'test_XXXXXXXX')
            # Получим актуальную информацию о платеже
            payment_info = Payment.find_one(some_data['paymentId'])
            if payment_info:
                payment_status = payment_info.status
                order.paid = True
                order.save()   
            else:
                # Обработка ошибок
                return HttpResponse(status=400)  # Сообщаем кассе об ошибке
        
        except Exception:
            # Обработка ошибок
            return HttpResponse(status=400)  # Сообщаем кассе об ошибке

    return HttpResponse(status=200)  # Сообщаем кассе, что все хорошо

