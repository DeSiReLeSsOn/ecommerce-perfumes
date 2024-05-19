from conftest import * 
from django.urls import reverse
from unittest.mock import patch
from django.http import HttpRequest
from shop.models import Product
from shop.views import product_detail
from cart.forms import CartAddProductForm
from cart.cart import Cart
from shop.recommender import Recommender
from django.template.loader import select_template 
from django.test import TestCase, Client




@pytest.mark.django_db
class TestProductListView:
    def test_product_list_view(self, client, test_category, test_product):
        """
        Тест проверяет, что список товаров отображается корректно.
        """
        url = reverse('shop:product_list')
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.context['page_obj']) == 1
        assert response.context['category'] is None
        assert response.templates[0].name == 'shop/product/list.html'
        assert response.context['sort_by'] == 'name'



    def test_product_list_by_category(self, client, test_category, test_product):
        """
        Тест проверяет, что список товаров фильтруется по категории.
        """
        test_product.category = test_category
        test_product.save()

        url = reverse('shop:product_list_by_category', kwargs={'category_slug': test_category.slug})
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.context['page_obj']) == 1
        assert response.context['category'] == test_category
        assert response.context['sort_by'] == 'name'
        assert response.templates[0].name == 'shop/product/list.html'

    def test_product_list_by_favorites(self, client, test_user, test_favorite):
        """
        Тест проверяет, что список товаров фильтруется по избранным товарам пользователя.
        """
        client.force_login(test_user)

        url = reverse('shop:product_list_favorites')
        response = client.get(url, {'is_favorites': 'True'})

        assert response.status_code == 200
        assert len(response.context['page_obj']) == 1
        assert response.context['category'] is None
        assert list(response.context['favorite_products']) == [test_favorite.product_id]

    def test_product_list_sort_by(self, client, test_product):
        """
        Тест проверяет, что список товаров сортируется корректно.
        """
        test_product_2 = Product.objects.create(
            category=test_product.category,
            name='test_product_2',
            slug='test-product-2',
            description='test_desc',
            available=True,
            price=100,
            volume='100ml'
        )
        test_product_3 = Product.objects.create(
            category=test_product.category,
            name='test_product_3',
            slug='test-product-3',
            description='test_desc',
            available=True,
            price=200,
            volume='100ml'
        )

        url = reverse('shop:product_list')

        # Сортировка по возрастанию цены
        response = client.get(url, {'sort_by': 'price-asc'})
        assert response.status_code == 200
        assert response.context['page_obj'][0] == test_product_2
        assert response.context['page_obj'][1] == test_product_3
        assert response.context['page_obj'][2] == test_product
        assert response.templates[0].name == 'shop/product/list.html'
        # Сортировка по убыванию цены
        response = client.get(url, {'sort_by': 'price-desc'})
        assert response.status_code == 200
        assert response.context['page_obj'][0] == test_product
        assert response.context['page_obj'][1] == test_product_3
        assert response.context['page_obj'][2] == test_product_2

    def test_product_list_pagination(self, client, test_product):
        """
        Тест проверяет, что пагинация списка товаров работает корректно.
        """
        for i in range(10):
            Product.objects.create(
                category=test_product.category,
                name=f'test_product_{i}',
                slug=f'test-product-{i}',
                description='test_desc',
                available=True,
                price=100,
                volume='100ml'
            )

        url = reverse('shop:product_list')

        # Проверка первой страницы
        response = client.get(url)
        assert response.status_code == 200
        
        
        assert response.templates[0].name == 'shop/product/list.html'
        # Проверка второй страницы
        response = client.get(url, {'page': 2})
        assert response.status_code == 200


@pytest.mark.django_db
class TestProductDetailView:
    def test_product_detail(self, test_product, client):
        url = reverse('shop:product_detail', kwargs={'id':test_product.id, 'slug':test_product.slug})

        response = client.get(url)
        

        assert response.status_code == 200
        assert response.context['product'] == test_product 
        assert response.templates[0].name == 'shop/product/detail.html'
        test_product.refresh_from_db()
        assert test_product.views_count == 1