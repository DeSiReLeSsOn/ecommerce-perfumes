import pytest
from django.contrib.auth.models import User
from shop.models import Category, Product, FavoriteProduct







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

@pytest.mark.django_db
def test_category_saving(db, test_category):
    assert Category.objects.all().count() == 1
    assert test_category.name == 'test_category'
    assert test_category.description == 'test_desc'
    assert str(test_category) == 'test_category'
    assert test_category.get_absolute_url() == f'/{test_category.slug}/'


@pytest.mark.django_db
def test_product_saving(db, test_category, test_product):
    assert Product.objects.all().count() == 1
    assert test_product.name == 'test_product'
    assert test_product.category == test_category
    assert test_product.price == 1300
    assert test_product.available == True
    assert test_product.volume == '100ml'
    assert test_product.description == 'test_desc'
    assert str(test_product) == 'test_product'
    assert test_product.get_absolute_url() == f'/{test_product.id}/{test_product.slug}/'

@pytest.mark.django_db
def test_favorite_saving(db, test_user, test_product, test_favorite):
    assert FavoriteProduct.objects.all().count() == 1
    assert test_favorite.user == test_user
    assert test_favorite.product == test_product
    