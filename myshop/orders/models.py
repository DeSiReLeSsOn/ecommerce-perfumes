from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator
from coupons.models import Coupon
from myshop import settings 
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model


User = get_user_model()


class Order(models.Model):
    full_name = models.CharField('ФИО', max_length=150, null=False, blank=False, default='')
    email = models.EmailField('Имейл', max_length=254)
    address = models.CharField('Адрес' ,max_length=250)
    postal_code = models.CharField('Почтовый код',max_length=20)
    phone = models.CharField('Телефон', null=True, validators=[
        RegexValidator(r'^\+?\d{1,15}$', 'Введите корректный номер телефона,без тире и пробелов') 
    ])
    created = models.DateTimeField("Создан",auto_now_add=True)
    updated = models.DateTimeField("Обновлен",auto_now=True)
    paid = models.BooleanField("Оплачен",default=False)
    yookassa_id = models.CharField(max_length=250, blank=True)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
            ordering = ['-created']
            indexes = [
                models.Index(fields=['-created']),
            ]


    def __str__(self):
        return f'Order {self.id}' 
    

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()


    def get_yookassa_url(self):
        if not self.yookassa_id:
            return ''
        return f'https://yookassa.ru/payments/{self.yookassa_id}'

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all()) 

    
    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)



class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
