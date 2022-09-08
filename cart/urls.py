from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', shopping_cart_view, name='shopping_cart_view'),
    path('add/<int:product_id>', add_to_cart_view, name='add_to_cart'),
    path('remove/<int:product_id>', remove_from_cart_view, name='remove_from_cart_view'),
    path('emptying_the_cart', emptying_all_of_the_products_from_the_cart, name='emptying_the_cart')
]
