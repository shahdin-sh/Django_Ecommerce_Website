from django.urls import path
from .views import *

urlpatterns = [
    path('', products_list_view, name='products_list_view'),
    path('<int:pk>', product_detail_view, name='product_detail_view'),
    path('<int:pk>/edit_comment/<int:comment_id>', edit_user_comments, name='edit_user_comments'),
]
