from django.urls import path
from .views import *

urlpatterns = [
    path('', products_list_view, name='products_list_view'),
    path('<int:pk>', product_detail_view, name='product_detail_view'),
    path('<int:pk>/edit_comment/<int:comment_id>', edit_use_comments, name='edit_user_comments'),
    path('<int:pk>/delete_comment/<int:comment_id>', delete_user_comments, name='delete_user_comments'),
]
