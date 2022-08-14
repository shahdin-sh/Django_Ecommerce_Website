from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import *


class TestProductUrls(SimpleTestCase):
    def test_product_list_view_is_resolved(self):
        url = reverse('products_list_view')
        self.assertEqual(resolve(url).func, products_list_view)

    def test_product_detail_view_is_resolved(self):
        url = reverse('product_detail_view', args=['1'])
        self.assertEqual(resolve(url).func, product_detail_view)
