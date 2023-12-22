from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from myshop.shop.models import Category, Product


class CategoryTest(TestCase):

    def create_category(self, name='test'):
        return Category.objects.create(name=name)

    def test_category_creating(self):
        s = self.create_category()
        self.assertTrue(isinstance(s, Category))
        self.assertEquals(s.__str__(), s.name)


class ProductTest(TestCase):
    def creating_category(self):
        self.category = Category.objects.create(name='parfums', slug='parfums',)

    def create_product(self, name='product', price=3000):
        return Product.objects.create(category=self.category, name=name, price=price, created=timezone.now(), updated=timezone.now())

    def test_product_creation(self):
        goods = self.create_product()
        self.assertTrue(isinstance(goods, Product))
        self.assertEquals(goods.__str__(), goods.name)

