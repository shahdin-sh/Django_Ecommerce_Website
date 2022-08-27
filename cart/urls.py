from django.urls import path
from .views import *

urlpatterns = [
    path('', shopping_cart_view, name='shopping_cart_view')
]
