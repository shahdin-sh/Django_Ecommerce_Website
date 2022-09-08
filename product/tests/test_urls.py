from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import *

# resolve ----> The resolve() function can be used for resolving URL paths to the corresponding view functions. It has the following signature: resolve (path, urlconf=None) path is the URL path you want to resolve.


class TestProductUrls(SimpleTestCase):
    # test urls by their names
    def test_product_list_view_is_resolved(self):
        url = reverse('products_list_view')
        self.assertEqual(resolve(url).func, products_list_view)

    def test_product_detail_view_is_resolved(self):
        url = reverse('product_detail_view', args=['1'])
        self.assertEqual(resolve(url).func, product_detail_view)

    def test_product_edit_comment_view_is_resolved(self):
        url = reverse('edit_user_comments', args=['1', '1'])
        self.assertEqual(resolve(url).func, edit_use_comments)

    def test_product_delete_comment_view_is_resolved(self):
        url = reverse('delete_user_comments', args=['1', '1'])
        self.assertEqual(resolve(url).func, delete_user_comments)

    def test_likes_on_products_view_is_resolved(self):
        url = reverse('user_likes_on_product', args=['1'])
        self.assertEqual(resolve(url).func, user_likes_on_products)

    def test_delete_likes_on_products_view_is_resolved(self):
        url = reverse('delete_user_likes_on_product', args=['1'])
        self.assertEqual(resolve(url).func, delete_user_likes_on_products)

    def test_user_likes_view(self):
        url = reverse('liked_products_view')
        self.assertEqual(resolve(url).func, liked_products_view)