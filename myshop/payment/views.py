from decimal import Decimal
#import yookassa
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponseRedirect, HttpResponse
from orders.models import Order
#from yookassa import Payment,Configuration
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
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

            session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)

    else:
        return render(request, 'payment/process.html', locals())


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
    







"""@csrf_exempt
def payment_process(request):
    Configuration.account_id = settings.YOO_KASSA_ACCOUNT_ID
    Configuration.secret_key = settings.YOO_KASSA_SECRET_KEY
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
                        reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(
                        reverse('payment:canceled'))
        payment = Payment.create({
            "amount": {
                "value": int(order.total * 100),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": success_url
            },
            "capture": True,
            "description": "Payment for order {}".format(order.id)
        })
        return redirect(payment.confirmation.confirmation_url, code=303)
    else:
        return render(request, 'payment/process.html', locals())
    

def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')"""




"""def payment_process(request):
    if request.method == 'POST':
        # Обработка данных платежа
        amount = request.POST['amount']
        currency = request.POST['currency']
        description = request.POST['description']

        # Создание объекта платежа
        payment = Payment.create(amount=amount, currency=currency, description=description)

        # Получение URL для оплаты
        payment_url = payment.confirmation_url

        # Перенаправление пользователя на страницу оплаты
        return HttpResponseRedirect(payment_url)

    return render(request, 'payment.html')


def webhook_view(request):
    webhook = Webhook(request.body, request.headers['Content-Type'])
    event = webhook.parse()

    # Обработка события оплаты
    if event.type == 'payment.succeeded':
        # Обновите статус заказа или выполните другие необходимые действия
        return HttpResponse(status=200)

    return HttpResponse(status=200)"""