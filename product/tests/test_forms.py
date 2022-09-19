from django.test import TestCase, Client
from ..forms import UserCommentsForm, GuestCommentForm
from accounts.models import CustomUserModel
from django.urls import reverse
from ..models import UserComments, Product
from cart.forms import AddToCartProductForm


class TestForm(TestCase):

    def setUp(self):
        self.user1 = CustomUserModel.objects.create(username='user1',
                                                    profile_avatar='/media/default/img_avatar.png')
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
        self.edit_comment = reverse('edit_user_comments',
                                    args=[self.user_comment_1.id, self.user_comment_1.product.id])
        self.delete_comment = reverse('delete_user_comments',
                                      args=[self.user_comment_1.id, self.user_comment_1.product.id])
        # registering the test session
        self.session = self.client.session
        self.session.get('guest_data')
        self.guest_data_session = self.session['guest_data'] = {
            'name': 'sam',
            'email': 'jhon@gmail.com'
        }

    # test user_comment_form
    def test_user_comments_form_data_validation(self):
        form = UserCommentsForm(data={
            'text': 'some_text',
        })
        self.assertTrue(form.is_valid())

    def test_user_comment_form_without_data(self):
        form = UserCommentsForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    # def test_product_detail_view_GET_contains_comment_form(self):
    #     comment_form = UserCommentsForm()
    #     response = self.client.get(self.products_detail_view)
    #     self.assertEqual(response.context['comment_form'], comment_form)

    # test_guest_comment_form
    def test_guest_comment_form_data_validation(self):
        form = GuestCommentForm(data={
            'name': self.session['guest_data']['name'],
            'email': self.session['guest_data']['email'],
            'text': 'something'
        })
        self.assertTrue(form.is_valid())

    def test_guest_comment_form_without_data(self):
        form = GuestCommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_guest_comment_form_set_initial_value_if_guest_session_exists(self):
        pass

    def test_guest_comment_form_set_name_and_email_value_as_a_guest_session(self):
        pass

    # test restricted add_to_cart_form for product_detail_view
    def test_add_to_cart_form_data_validation(self):
        form = AddToCartProductForm(data={
            'quantity': 1,
        }, product_stock=self.product_1.number_of_products)
        self.assertTrue(form.is_valid())

    def test_add_to_cart_form_without_data(self):
        form = AddToCartProductForm(data={}, product_stock=self.product_1.number_of_products)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

