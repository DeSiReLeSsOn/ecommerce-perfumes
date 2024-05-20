import pytest
from cart.forms import CartAddProductForm
from django.urls import reverse 
from shop.tests.conftest import *
from cart.cart import Cart


@pytest.mark.django_db
class TestCartAddForm:
    def test_validation_data(self, client):
        data = {'quantity': 10, 'override': False}


        form = CartAddProductForm(data=data) 

        assert form.is_valid()
        assert form.cleaned_data['quantity'] == 10 
        assert form.cleaned_data['override'] == False 


        data = {'quantity': 0, 'override': False}
        form = CartAddProductForm(data=data)
        assert not form.is_valid()
        assert 'quantity' in form.errors
        assert 'override' not in form.errors

        data = {'quantity': -1, 'override': False}
        form = CartAddProductForm(data=data)
        assert not form.is_valid()
        assert 'quantity' in form.errors
        assert 'override' not in form.errors

    def test_quantity_choices(self):
        expected_choices = [(i, str(i)) for i in range(1, 21)]
        form = CartAddProductForm()
        assert form.fields['quantity'].choices == expected_choices



