from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal





def order_yookassa_payment(obj):
    url = obj.get_yookassa_url()
    if obj.yookassa_id:
        html = f'<a href="{url}" target="_blank">{obj.yookassa_id}</a>'
        return mark_safe(html)
    return ''
order_yookassa_payment.short_description = 'Yookassa payment'
#@admin.register(Order)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']  


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name_plural}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    
    field_names = ['ID Заказа', 'Покупатель', 'ФИО', 'Email', 'Адрес', 'Почтовый индекс', 'Телефон', 'Создан', 'Оплачен', 'Купон', 'Скидка', 'Сумма заказа в рублях', 'Товар', 'Количество']
    writer.writerow(field_names)

    total_orders_cost = Decimal(0)
    total_orders_paid = Decimal(0) 
    

    for obj in queryset:
        items_info = [(item.product.name, item.quantity) for item in obj.items.all()]
        for item_info in items_info:
            data_row = [
                obj.id,
                obj.user.username if obj.user else 'Не зарегистрирован',
                obj.full_name,
                obj.email,
                obj.address,
                obj.postal_code,
                obj.phone,
                obj.created.strftime('%d/%m/%Y %H:%M:%S'),
                'Да' if obj.paid else 'Нет',  
                obj.coupon.code if obj.coupon else 'Без купона',
                obj.discount,
                obj.get_total_cost(),
                item_info[0],
                item_info[1]
            ]
            writer.writerow(data_row)

        total_orders_cost += obj.get_total_cost()
        total_orders_paid = total_orders_paid + obj.get_total_cost() if obj.paid else total_orders_paid + 0 

    writer.writerow([f'Общая стоимость всех заказов = {total_orders_cost} руб'])

    writer.writerow([f'Общая стоимость всех оплаченных заказов = {total_orders_paid} руб'])
    
    return response

export_to_csv.short_description = 'Преобразовать в CSV'


def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">Обзор</a>')

"""def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'"""

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email',
                    'address', 'postal_code', 'phone', 'paid',
                    order_yookassa_payment, 'created', 'updated', 'get_total_cost', order_detail,]# order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
    list_per_page = 6
    order_detail.short_description = 'Детали заказа'


