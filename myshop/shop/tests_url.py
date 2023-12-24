from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import  *


class TestUrls(SimpleTestCase):


    def test_list_url(self):
        """Тест на получение URL-адреса для списка продуктов"""
        url = reverse('shop:product_list')
        self.assertEquals(resolve(url).func, product_list)


    def test_list_by_category_url(self):
        """Тест на получение URL-адреса для списка продуктов по категориям"""
        url = reverse('shop:product_list_by_category', args=['any-slug'])
        self.assertEquals(resolve(url).func, product_list)


    def test_detail_url(self):
        """Тест на получение URL-адреса деталей продукта"""
        url = reverse('shop:product_detail', kwargs={'id': 1, 'slug': 'any_slug'})
        self.assertEquals(resolve(url).func, product_detail)