
import pytest
from django.contrib.auth.models import User
from shop.models import Category, Product, FavoriteProduct
from banner.models import Banner







@pytest.fixture
def test_category():
    category = Category.objects.create(name='test_category', description='test_desc', slug='test-category')
    return category

@pytest.fixture
def test_product(test_category):
    product = Product.objects.create(
        category=test_category,
        name='test_product',
        slug='test-product',
        description='test_desc',
        available=True,
        price=1300,
        volume='100ml'
    )
    return product

@pytest.fixture
def test_user():
    user = User.objects.create_user(username='test_user', password='test_password')
    return user

@pytest.fixture
def test_favorite(test_user, test_product):
    favorite_product = FavoriteProduct.objects.create(
        user=test_user,
        product=test_product
    )
    return favorite_product 

@pytest.fixture
def test_banner():
    banner = Banner.objects.create(advertisement_text="Test_Banner", image="test.jpg", is_active=True, link='#')
    return banner