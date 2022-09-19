from django.urls import path
from .views import *

urlpatterns = [
    path('', products_list_view, name='products_list_view'),
    path('<int:pk>', product_detail_view, name='product_detail_view'),
    path('<int:pk>/guest_comments', comment_system_for_guests, name='guest_comment_system'),
    path('<int:pk>/edit_comment/<int:comment_id>', edit_user_comments, name='edit_user_comments'),
    path('<int:pk>/delete_comment/<int:comment_id>', delete_user_comments, name='delete_user_comments'),
    path('<int:pk>/like_product', user_likes_on_products, name='user_likes_on_product'),
    path('<int:pk>/delete_like_product', delete_user_likes_on_products, name='delete_user_likes_on_product'),
    path('liked_products', liked_products_view, name='liked_products_view'),
]
