import pytest 
from shop.tests.conftest import *  
from orders.forms import OrderCreateForm

@pytest.mark.django_db
class TestOrderForms:
    def test_order_form_fields(self, client, test_order):
        data = {'full_name': test_order.full_name,
                'email': test_order.email,
                'address': test_order.address,
                'postal_code': test_order.postal_code,
                'phone': test_order.phone}
        
        form = OrderCreateForm(data=data)


        assert form.is_valid()
        assert form.cleaned_data['full_name'] == 'Ronaldo' 
        assert form.cleaned_data['email'] == 'test@gmail.com'
        assert form.cleaned_data['address'] == 'Pogtugal'
        assert form.cleaned_data['postal_code'] == '123456'
        assert form.cleaned_data['phone'] == '+79595628159'   