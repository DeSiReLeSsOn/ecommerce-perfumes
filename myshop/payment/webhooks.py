import json
from django.http import HttpResponse
from yookassa import Configuration, Payment, Webhook
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory
from yookassa.domain.common import SecurityHelper
from django.views.decorators.csrf import csrf_exempt
from .tasks import payment_completed
from orders.models import Order
from myshop import settings 
from django.shortcuts import render, redirect, reverse, get_object_or_404



@csrf_exempt
def yookassa_webhook(request):
    try:
        event_json = json.loads(request.body)
        event = event_json.get('event')

        if event == "payment.succeeded":
            payment_object = event_json.get('object')
            description = payment_object.get('description')

            # Извлекаем order_id 
            if description:
                try:
                    order_id = int(description.split()[-1])
                except ValueError:
                    # Обработка случая, если описание не содержит order_id
                    return HttpResponse(status=400)  # Возвращаем 400
            else:
                return HttpResponse(status=400)  # Возвращаем 400

            # Получаем заказ из базы данных
            order = get_object_or_404(Order, id=order_id)

            # Проверяем, был ли заказ уже оплачен 
            if not order.paid:
                order.paid = True
                order.save()
                # Вызываем таск для завершения платежа
                payment_completed.delay(order.id)
                return HttpResponse(status=200)  # Возвращаем 200
            else:
                # Заказ уже оплачен - возвращаем 200, чтобы подтвердить получение уведомления
                return HttpResponse(status=200)

        else:
            return HttpResponse(status=404)

    except KeyError as e:
        # Выводим информацию об ошибке в лог
        print(f"KeyError: {e}")
        return HttpResponse(status=400)

    except Order.DoesNotExist:
        # Выводим информацию об ошибке в лог
        print(f"Order.DoesNotExist: {e}")
        return HttpResponse(status=400)

    except Exception as e:
        # Выводим информацию об ошибке в лог
        print(f"Exception: {e}")
        return HttpResponse(status=500)  # Возвращаем 500 для ошибки сервера

    return HttpResponse(status=405)


