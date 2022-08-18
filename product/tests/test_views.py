from django.test import TestCase, Client
from django.urls import reverse
from ..models import UserComments, Product


class TestView(TestCase):

    def setUp(self):
        self.client = Client
        self.product_1 = Product.objects.create(
            product_title='product1',
            product_description='random_description',
            product_datetime_created='some_date',
            product_datetime_modified='some_modified_data',
            product_price='10000',
            product_existence='True',
            product_cover='default/product_sample.png',
        )
        self.products_list_view = reverse('products_list_view')
        self.products_detail_view = reverse('product_detail_view', args=[self.product_1.id])

    def test_product_list_view_GET(self):
        client = Client()
        response = client.get(self.products_list_view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/products_list_view.html')

    def test_product_detail_view_GET(self):
        client = Client()
        response = client.get(self.products_detail_view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product_detail_view.html')
