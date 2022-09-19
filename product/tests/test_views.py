from django.test import TestCase, Client
from django.urls import reverse
from ..models import UserComments, Product
from accounts.models import CustomUserModel
from ..forms import UserCommentsForm
from django.contrib.messages import get_messages
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404

# the most complicated tests, train then come back and add changes


class TestView(TestCase):

    def setUp(self):
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
        self.user_comment_1 = UserComments.objects.create(
            text='text1',
            product=self.product_1,
            user=self.user1,
            datetime_created='some_date',
            datetime_modified='some_modified_date',
            is_active='True',
            rate='good',
        )
        self.products_list_view = reverse('products_list_view')
        self.products_detail_view = reverse('product_detail_view', args=[self.product_1.id])
        self.guest_comment_system = reverse('guest_comment_system', args=[self.product_1.id])
        self.edit_comment = reverse('edit_user_comments', args=[self.user_comment_1.id, self.user_comment_1.product.id])
        self.delete_comment = reverse('delete_user_comments', args=[self.user_comment_1.id, self.user_comment_1.product.id])

    # product_list_view tests
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

    # product detail view tests
    def test_product_detail_view_GET(self):
        client = Client()
        response = client.get(self.products_detail_view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product_detail_view.html')

    def test_product_detail_view_objects_are_exists(self):
        client = Client()
        response = client.get(self.products_detail_view)
        self.assertContains(response, self.product_1 and self.user_comment_1)

    def test_product_detail_view_POST_data_comment_object(self):
        client = Client()
        client.force_login(self.user1)
        data = {
            'text': 'some_random_text',
        }
        response = client.post(self.products_detail_view, data=data)
        self.assertEqual(UserComments.objects.filter(text='some_random_text').count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_product_detail_view_redirect_to_the_desired_url(self):
        client = Client()
        response = client.post(self.products_detail_view)
        self.assertRedirects(response, self.products_detail_view)

    def test_product_detail_view_POST_no_data(self):
        client = Client()
        response = client.post(self.products_detail_view, data={})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserComments.objects.filter(text='some_random_text').count(), 0)

    def test_product_detail_view_creating_messages(self):
        client = Client()
        response = client.post(self.products_detail_view)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "success")
        self.assertEqual(all_messages[0].message, _('your comment saved successfully'))

    # test comment system for guests
    def test_comment_system_for_guests_only_allows_POST_request(self):
        client = Client()
        response = client.get(self.guest_comment_system)
        self.assertEqual(response.status_code, 405)

    # def test_comment_system_for_guests_contains_guest_session(self):
    #     client = Client()
    #     # initializing guest session
    #     session = client.session
    #     session.get('guest_data')
    #     if not session.get('guest_data'):
    #         session['guest_data'] = {}
    #     guest_data = session['guest_data']
    #     response = client.post(self.guest_comment_system)
    #     self.assertContains(response, guest_data)

    def test_comment_system_for_guests_redirect_to_desired_url(self):
        client = Client()
        response = client.post(self.guest_comment_system)
        self.assertRedirects(response, self.products_detail_view, status_code=302)

    # test edit_user_comments
    def test_edit_user_comments_GET_if_user_authenticated(self):
        client = Client()
        # handle login required
        client.force_login(self.user1)
        response = client.get(self.edit_comment)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/edit_product_comments.html')

    def test_edit_user_comments_login_required(self):
        client = Client()
        response = client.get(self.edit_comment)
        self.assertEqual(response.status_code, 302)

    def test_edit_user_comments_creating_messages(self):
        client = Client()
        client.force_login(self.user1)
        response = client.post(self.edit_comment)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "success")
        self.assertEqual(all_messages[0].message, _('your comment changed successfully'))

    def test_edit_user_comments_redirects_to_desired_url(self):
        client = Client()
        client.force_login(self.user1)
        response = client.post(self.edit_comment)
        self.assertRedirects(response, self.products_detail_view)

    # test delete_user_comments
    def test_delete_user_comments_GET_if_user_authenticated(self):
        client = Client()
        client.force_login(self.user1)
        response = client.get(self.delete_comment)
        self.assertEqual(response.status_code, 200)

    def test_delete_user_comments_login_required(self):
        client = Client()
        response = client.get(self.delete_comment)
        self.assertEqual(response.status_code, 302)

    def test_delete_user_comments_creating_messages(self):
        client = Client()
        client.force_login(self.user1)
        response = client.post(self.delete_comment)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "success")
        self.assertEqual(all_messages[0].message, _('your comment deleted successfully'))

    def test_delete_user_comments_redirects_to_desired_url(self):
        client = Client()
        client.force_login(self.user1)
        response = client.post(self.delete_comment)
        self.assertRedirects(response, self.products_detail_view)

    # def test_delete_user_comments_DELETE(self):
    #     client = Client()
    #     client.force_login(self.user1)
    #     UserComments.objects.create(
    #         user=self.user1,
    #         product=self.product_1,
    #         text='test_comment_text'
    #     )
    #     response = client.post(self.delete_comment, data={
    #         'text': 'test_comment_text',
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(UserComments.objects.filter(text='test_comment_text').count(), 0)

    # def test_delete_user_comments_DELETE_no_data(self):
    #     client = Client()
    #     UserComments.objects.create(
    #         text='test_comment_text',
    #         product=self.product_1,
    #         user=self.user1,
    #     )
    #     response = client.delete(self.delete_comment)
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(UserComments.objects.filter(user=self.user1, text='test_comment_text').count(), 1)
