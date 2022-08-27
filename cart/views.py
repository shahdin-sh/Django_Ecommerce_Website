from django.shortcuts import render


def shopping_cart_view(request):
    return render(request, 'cart/shopping_cart.html')
