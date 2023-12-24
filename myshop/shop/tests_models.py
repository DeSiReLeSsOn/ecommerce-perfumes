from django.test import TestCase
from django.urls import reverse
from .models import Category

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
        )
    def test_str(self):
        self.assertEqual(str(self.category), 'Test Category')
    def test_get_absolute_url(self):
        expected_url = reverse('shop:product_list_by_category', args=['test-category'])
        self.assertEqual(self.category.get_absolute_url(), expected_url)