from django.shortcuts import render, get_object_or_404, redirect
from product.models import Product
from .cart import ShoppingCart
from .forms import AddToCartProductForm


def shopping_cart_view(request):
    shopping_cart = ShoppingCart(request)
    # dic for context
    dic = {
        'shopping_cart': shopping_cart,
    }
    return render(request, 'cart/shopping_cart.html', dic)


def add_to_cart_view(request, product_id):
    shopping_cart = ShoppingCart(request)
    product = get_object_or_404(Product.product_manager, id=product_id)
    # rendering our form
    form = AddToCartProductForm(request.POST, product_stock=product.number_of_products)
    if request.method == 'POST':
        if form.is_valid():
            # clean data:  Django creates an attribute called cleaned_data ,
            # a dictionary which contains cleaned data only from the fields which have passed the validation tests.
            cleaned_data = form.cleaned_data
            quantity = cleaned_data['quantity']
            shopping_cart.add_to_cart(product, quantity)
        return redirect('cart:shopping_cart_view')

