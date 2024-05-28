from django.urls import path
from payment import views
from payment import webhooks

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('webhooks/', views.yookassa_webhook, name='yookassa_webhook'),
    path('completed/', views.payment_completed, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled'),

]