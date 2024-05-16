import pytest
from django.contrib.auth.models import User
from shop.models import Category, Product, FavoriteProduct



@pytest.fixture
def category():
    return Category.objects.create(
        name='Тестовая категория',
        slug='test-category',
        description='Описание тестовой категории'
    )

@pytest.fixture
def product(category):
    return Product.objects.create(
        category=category,
        name='Тестовый продукт',
        slug='test-product',
        description='Описание тестового продукта',
        price=100.00,
        volume='100ml'
    )

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')

def test_category_creation(db, category):
    assert str(category) == 'Тестовая категория'
    assert category.get_absolute_url() == '/shop/test-category/'

def test_product_creation(db, product):
    assert str(product) == 'Тестовый продукт'
    assert product.get_absolute_url() == f'/shop/{product.id}/test-product/'

def test_favorite_product_creation(db, user, product):
    favorite_product = FavoriteProduct.objects.create(user=user, product=product)
    assert favorite_product.user == user
    assert favorite_product.product == product

@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(
        name='Тестовая категория',
        slug='test-category',
        description='Описание тестовой категории'
    )
    assert str(category) == 'Тестовая категория'
    assert category.get_absolute_url() == '/test-category/'

@pytest.mark.django_db
def test_product_creation():
    category = Category.objects.create(
        name='Тестовая категория',
        slug='test-category',
        description='Описание тестовой категории'
    )
    product = Product.objects.create(
        category=category,
        name='Тестовый продукт',
        slug='test-product',
        description='Описание тестового продукта',
        price=100.00,
        volume='100ml'
    )
    assert str(product) == 'Тестовый продукт'
    assert product.get_absolute_url() == f'/{product.id}/test-product/'

@pytest.mark.django_db
def test_favorite_product_creation():
    user = User.objects.create_user(username='testuser', password='testpassword')
    category = Category.objects.create(
        name='Тестовая категория',
        slug='test-category',
        description='Описание тестовой категории'
    )
    product = Product.objects.create(
        category=category,
        name='Тестовый продукт',
        slug='test-product',
        description='Описание тестового продукта',
        price=100.00,
        volume='100ml'
    )
    favorite_product = FavoriteProduct.objects.create(user=user, product=product)
    assert favorite_product.user == user
    assert favorite_product.product == product
