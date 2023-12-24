from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import  *


class TestUrls(SimpleTestCase):


    def test_list_url(self):
        url = reverse('shop:product_list')
        self.assertEquals(resolve(url).func, product_list)


    def test_list_by_category_url(self):
        url = reverse('shop:product_list_by_category', args=['any-slug'])
        self.assertEquals(resolve(url).func, product_list)


