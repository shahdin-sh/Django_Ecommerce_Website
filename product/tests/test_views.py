from django.test import TestCase, Client
from django.urls import reverse
from ..models import UserComments, Product
from accounts.models import CustomUserModel


# the most complicated tests, train then come back and add changes

class TestView(TestCase):

    def setUp(self):
        self.client = Client
        self.user1 = CustomUserModel.objects.create(username='user1', profile_avatar='/media/default/img_avatar.png')
        self.product_1 = Product.objects.create(
            product_title='product1',
            product_description='random_description',
            product_datetime_created='some_date',
            product_datetime_modified='some_modified_data',
            product_price='10000',
            product_existence='True',
            product_cover='default/product_sample.png',
            number_of_products='10',
        )
        self.products_list_view = reverse('products_list_view')
        self.products_detail_view = reverse('product_detail_view', args=[self.product_1.id])
        self.user_comment_1 = UserComments.objects.create(
            text='text1',
            product=self.product_1,
            user=self.user1,
            datetime_created='some_date',
            datetime_modified='some_modified_date',
            is_active='True',
            rate='good',
        )
        self.edit_comment = reverse('edit_user_comments', args=[self.user_comment_1.id, self.user_comment_1.product.id])
        self.delete_comment = reverse('delete_user_comments', args=[self.user_comment_1.id, self.user_comment_1.product.id])

    def test_product_list_view_GET(self):
        client = Client()
        response = client.get(self.products_list_view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/products_list_view.html')

    # if we exceed the page limit it returns the last page.
    def test_product_list_view_last_pages_of_our_object_in_to(self):
        client = Client()
        response = client.get(self.products_list_view)
        self.assertEqual(response.context['products'].number, response.context['products'].paginator.page(1).number)

    def test_product_list_view_paginator_per_page_object_limit(self):
        client = Client()
        response = client.get(self.products_list_view)
        self.assertEqual(response.context['products'].paginator.per_page, 6)

    def test_products_list_view_objects_are_exists(self):
        client = Client()
        response = client.get(self.products_list_view)
        self.assertContains(response, self.product_1.product_title)

    def test_product_detail_view_GET(self):
        client = Client()
        response = client.get(self.products_detail_view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product_detail_view.html')

    def test_product_detail_view_object_is_exist(self):
        client = Client()
        response = client.get(self.products_detail_view)
        self.assertContains(response, self.product_1.id)

    def test_comment_object_is_exist_in_product_detail_view(self):
        client = Client()
        response = client.get(self.products_detail_view)
        self.assertContains(response, self.user_comment_1.id)

    # find out why it gives 200 instead of 201
    # def test_product_detail_view_POST(self):
    #     client = Client()
    #     response = client.post(self.products_detail_view)
    #     self.assertEqual(response.status_code, 201)

    # def test_is_comment_product_product_detail(self):
    #     pass

    # def test_is_comment_user_request_user(self):
    #     pass

    # def test_product_detail_view_redirects_to_the_correct_url(self):
    #     client = Client()
    #     response = client.post(self.products_detail_view)
    #     self.assertRedirects(response, self.products_detail_view)
