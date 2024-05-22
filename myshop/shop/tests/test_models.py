from conftest import *


pytestmark = pytest.mark.django_db

def test_category_saving(test_category):
    assert Category.objects.all().count() == 1
    assert test_category.name == 'test_category'
    assert test_category.description == 'test_desc'
    assert str(test_category) == 'test_category'
    assert test_category.get_absolute_url() == f'/{test_category.slug}/'

def test_product_saving(test_product):
    assert Product.objects.all().count() == 1
    assert test_product.name == 'test_product'
    assert test_product.category == test_product.category
    assert test_product.price == 1300
    assert test_product.available == True
    assert test_product.volume == '100ml'
    assert test_product.description == 'test_desc'
    assert str(test_product) == 'test_product'
    assert test_product.get_absolute_url() == f'/{test_product.id}/{test_product.slug}/'

def test_favorite_saving(test_favorite):
    assert FavoriteProduct.objects.all().count() == 1
    assert test_favorite.user == test_user
    assert test_favorite.product == test_product
