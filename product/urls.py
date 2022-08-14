from django.urls import path
from .views import *

urlpatterns = [
    path('', products_list_view, name='products_list_view'),
    path('<int:pk>', product_detail_view, name='product_detail_view'),
]
