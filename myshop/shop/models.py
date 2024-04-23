from django.db import models
from django.urls import reverse
from django.db.models.query import QuerySet
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)
    image = models.ImageField(upload_to='brands/%Y/%m',
                              blank=True, verbose_name='Фото бренда')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='Продукт')
    slug = models.SlugField(max_length=200, verbose_name="Слаг")
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True, verbose_name='Фото товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='В наличии/не в наличии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Товар создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Товар обновлен')
    volume = models.CharField(max_length=10, verbose_name="Обьем флакона", blank=False, default="50ml")




    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug]) 
    



class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)




