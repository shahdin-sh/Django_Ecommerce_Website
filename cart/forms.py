from django import forms


class AddToCartProductForm(forms.Form):

    def __init__(self, *args, **kwargs):
        product_stock = kwargs.pop('product_stock')
        super(AddToCartProductForm, self).__init__(*args, **kwargs)
        QUANTITY_CHOICES = [(i, str(i)) for i in range(1, int(product_stock) + 1)]
        self.fields['inplace'] = forms.BooleanField(required=False, widget=forms.HiddenInput)
        self.fields['quantity'] = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int, required=True)




