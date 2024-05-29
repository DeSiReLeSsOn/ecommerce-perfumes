import pytest
from django.contrib.auth.models import User
from shop.models import Category, Product, FavoriteProduct
from banner.models import Banner 
from orders.models import *
from coupons.models import Coupon
from reviews.models import Review, Comment
import datetime
from django.utils import timezone
from cart.cart import Cart
from django.urls import reverse






@pytest.fixture
def admin_user(db):
    User = get_user_model()
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
    )
    return admin




@pytest.fixture
def test_category(db):
    category = Category.objects.create(name='test_category', description='test_desc', slug='test-category')
    return category

@pytest.fixture
def test_product(db ,test_category):
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
def test_user(db):
    user = User.objects.create_user(username='test_user', password='test_password', email='test@gmail.com')
    return user

@pytest.fixture
def test_favorite(db ,test_user, test_product):
    favorite_product = FavoriteProduct.objects.create(
        user=test_user,
        product=test_product
    )
    return favorite_product 

@pytest.fixture
def test_banner(db):
    banner = Banner.objects.create(advertisement_text="Test_Banner", image="test.jpg", is_active=True, link='#')
    return banner 








@pytest.fixture
def test_order(db ,test_user):
    order = Order.objects.create(user=test_user, 
                                 full_name='Ronaldo', 
                                 email='test@gmail.com', 
                                 address='Pogtugal', 
                                 postal_code='123456',
                                 phone='+79595628159',
                                 )
    return order 


@pytest.fixture
def test_order_item(db ,test_order, test_product, test_user):
    order_item = OrderItem.objects.create(
        order=test_order,
        product=test_product, 
        price=test_product.price, 
        quantity=1, 
        user=test_user
    )
    return order_item 





@pytest.fixture
def test_coupon(db):
    coupon = Coupon.objects.create(
        code='1111', 
        valid_from=timezone.now(),
        valid_to=timezone.now() + datetime.timedelta(days=1),
        discount=10, 
        active=True
    )
    return coupon




@pytest.fixture
def test_order_with_coupon(db, test_user, test_coupon):
    order = Order.objects.create(user=test_user, 
                                 full_name='Ronaldo', 
                                 email='test@gmail.com', 
                                 address='Pogtugal', 
                                 postal_code='123456',
                                 phone='+79595628159',
                                 coupon=test_coupon
                                 )
    return order  


@pytest.fixture
def test_order_item_with_coupon(db, test_order_with_coupon, test_product, test_user):
    order_item = OrderItem.objects.create(
        order=test_order_with_coupon,
        product=test_product, 
        price=test_product.price, 
        quantity=1, 
        user=test_user
    )
    return order_item  



@pytest.fixture
def test_cart(db, client, test_category):
    test_product = Product.objects.create(
        name='test_product',
        price=100,
        description='Test product description',
        category=test_category,
        image=None,
        available=True,
    )
    cart = Cart(client)
    cart.add(test_product, quantity=2)
    cart.save()
    return cart 


@pytest.fixture
def test_review(db, client, test_user):
    test_review = Review.objects.create(
        user=test_user,
        text='Test_review'
    )
    return test_review 


@pytest.fixture
def test_comment_review(db, client, test_review, test_user):
    test_comment = Comment.objects.create(
        review=test_review,
        user=test_user, 
        text='Test_comment_review'
    )
    return test_comment