from django.test import Client, TestCase
from django.urls import reverse
from .models import *


class TestViews(TestCase):

    def setUp(self):
        """Создаем клиента для взаимодействия с сервером,создаем категорию и товар"""
        self.client = Client()
        self.category = Category.objects.create(name='fastfood', slug='fastfood1',)
        self.product = Product.objects.create(category=self.category, id=20, name='testproduct', slug='testproduct',
        description='my test product', image='media/products/2023/10/22/dior.jpg', price=30)

    def test_product_list_view(self):
        """Тест на отображение списка товаров,код ответа = 200,означает запрос успешно обработан и возвращен без ошибок"""
        response = self.client.get(reverse('shop:product_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')

    def test_product_list_by_category_view(self):
        """Тест на отображение списка товаров по категориям"""
        response = self.client.get(reverse('shop:product_list_by_category', kwargs={"category_slug": "fastfood1"}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')

    def test_product_detail_view(self):
        """Тест на отображение подробностей о товаре"""
        response = self.client.get(reverse('shop:product_detail', kwargs={'id': 20, 'slug': 'testproduct'}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/detail.html')

    def test_product_detail_view_error(self):
        """Тест на недоступность получения деталей для несуществующего товара"""
        response = self.client.get(reverse('shop:product_detail', kwargs={'id': 21, 'slug': 'nottestproduct'}))
        self.assertEquals(response.status_code, 404)
