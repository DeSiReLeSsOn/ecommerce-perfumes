import pytest 
from shop.tests.conftest import * 



@pytest.mark.django_db
class TestOrderModel:
    def test_order_fields(self, test_order, test_user, test_order_item):
        assert Order.objects.all().count() == 1 
        assert test_order.user == test_user 
        assert test_order.full_name == 'Ronaldo'
        assert test_order.email == 'test@gmail.com'
        assert test_order.address == 'Pogtugal'
        assert test_order.postal_code == '123456'
        assert test_order.phone == '+79595628159'
        assert str(test_order) == f'Order {test_order.id}'
        assert test_order.get_total_cost() == test_order_item.price 
        assert test_order.get_discount() == 0
        assert test_order.get_total_cost_before_discount() == test_order_item.price 

    def test_order_item(self, test_order_item, test_user, test_product, test_order):
        assert test_order_item.order == test_order 
        assert test_order_item.product == test_product
        assert test_order_item.price == test_product.price
        assert test_order_item.quantity == 1
        assert test_order_item.user == test_user
        assert str(test_order_item) == f'{test_order_item.id}'
        assert test_order_item.get_cost() == test_order_item.quantity * test_order_item.price