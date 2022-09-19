from django.test import TestCase, Client
from django.urls import reverse
from ..models import UserComments, Product, ProductManager, CustomCommentManager
from accounts.models import CustomUserModel


class TestModel(TestCase):
    # DUPLICATE CODE NOT FINE
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
        self.delete_comment = reverse('delete_user_comments',
                               args=[self.user_comment_1.id, self.user_comment_1.product.id])

    # test for Product class
    def test_Product_str_method(self):
        self.assertEqual(self.product_1.__str__(), self.product_1.product_title)

    def test_Product_get_absolute_url(self):
        self.assertEqual(self.product_1.get_absolute_url(), self.products_detail_view)

    def test_Product_custom_manager_queryset(self):
        pass

    # test for Comment class
    def test_UserComment_str_method(self):
        self.assertEqual(self.user_comment_1.__str__(), self.user_comment_1.text)

    def test_UserComment_get_absolute_url(self):
        self.assertEqual(self.product_1.get_absolute_url(), self.products_detail_view)

    def test_UserComment_custom_manager_queryset(self):
        pass