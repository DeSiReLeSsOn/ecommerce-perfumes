from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import  *


class TestUrls(SimpleTestCase):


    def test_list_url(self):
        url = reverse('shop:product_list')
        self.assertEquals(resolve(url).func, product_list)