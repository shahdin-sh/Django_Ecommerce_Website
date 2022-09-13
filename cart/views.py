from django.shortcuts import render, get_object_or_404, redirect
from product.models import Product
from .cart import ShoppingCart
from .forms import AddToCartProductForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import Http404


def shopping_cart_view(request):
    shopping_cart = ShoppingCart(request)
    if not shopping_cart.is_cart_empty():
        for item in shopping_cart:
            item['product_update_quantity_form'] = AddToCartProductForm(initial={
                'quantity': item['quantity'],
                'inplace': True,
            }, product_stock=item['product_obj'].product_price)
        # dic for context
        dic = {
            'shopping_cart': shopping_cart,
        }
        return render(request, 'cart/shopping_cart.html', dic)
    else:
        raise Http404()


@require_POST
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
            shopping_cart.add_to_cart(product, quantity, replace_current_quantity=cleaned_data['inplace'])
            if cleaned_data['inplace']:
                messages.success(request, 'product quantity updated successfully')
            elif not cleaned_data['inplace']:
                messages.success(request, 'this product added to your cart successfully')
            # check if quantity of product is bigger than a number of products in database
        return redirect('cart:shopping_cart_view')


def remove_from_cart_view(request, product_id):
    shopping_cart = ShoppingCart(request)
    product = get_object_or_404(Product.product_manager, id=product_id)
    shopping_cart.delete_from_cart(product)
    messages.warning(request, 'this product deleted from your cart')
    return redirect('product_detail_view', pk=product_id)


def emptying_all_of_the_products_from_the_cart(request):
    shopping_cart = ShoppingCart(request)
    shopping_cart.emptying_the_cart()
    return redirect('products_list_view')
