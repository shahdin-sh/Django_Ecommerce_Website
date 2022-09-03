from .cart import ShoppingCart


def shopping_cart(request):
    return {'shopping_cart': ShoppingCart(request)}