from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Submit
from crispy_forms.bootstrap import PrependedText, PrependedAppendedText

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int, label='Количество')
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Div(
                    PrependedAppendedText('quantity',
                                          PrependedText('<button class="btn btn-outline-primary js-btn-minus" type="button">&minus;</button>',
                                                        '<button class="btn btn-outline-primary js-btn-plus" type="button">&plus;</button>'),
                                          css_class='input-group mb-3')
                ),
                css_class='col-auto'
            ),
            Submit('submit', 'Купить парфюмерную продукцию', css_class='btn btn-dark btn-block')
        )