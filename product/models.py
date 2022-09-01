from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


# Managers
class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(product_existence=True, number_of_products__gt=0)


class CustomCommentManager(models.Manager):
    def get_queryset(self):
        return super(CustomCommentManager, self).get_queryset().filter(is_active=True, parent__isnull=True)


# Models
class Product(models.Model):
    all_available_product_classification = [
        ('Uncategorized', 'UN'),
        ('Clothing and fashion', 'CAF'),
        ('Supermarket Items', 'SI'),
        ('Home Appliances', 'HA'),
        ('Toys', 'TY'),
        ('Books', 'BO'),
    ]
    product_title = models.CharField(max_length=100, verbose_name=_('title'))
    product_description = models.TextField(verbose_name=_('description'))
    product_datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('datetime_created'))
    product_datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('datetime_modified'))
    product_price = models.PositiveIntegerField(default=0, verbose_name=_('price'))
    product_existence = models.BooleanField(default=True, verbose_name=_('existence'))
    product_cover = models.ImageField(upload_to='product/', default='default_product/shop_cart.jpg',
                                      verbose_name=_('cover'))
    number_of_products = models.IntegerField(default=10, verbose_name=_('numbers'))
    product_classification = models.CharField(choices=all_available_product_classification,
                                              max_length=200, default=all_available_product_classification[5],
                                              verbose_name=_('classification'))
    product_likes = models.ManyToManyField(get_user_model(), related_name='likes_on_products', blank=True, null=True,
                                           verbose_name=_('likes_on_product'))

    def __str__(self):
        return self.product_title

    def likes_on_product(self):
        return self.product_likes.count()

    def get_absolute_url(self):
        return reverse('product_detail_view', args=[self.id])

    # Product Manager
    objects = models.Manager()  # django default manager
    product_manager = ProductManager()


class UserComments(models.Model):
    PRODUCT_STARS = [
        ('5', _('perfect')),
        ('4', _('good')),
        ('3', _('normal')),
        ('2', _('bad')),
        ('1', _('Very bad')),
    ]
    text = models.TextField(verbose_name=_('comment_text'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('comment_datetime_created'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('comment_datetime_modified'))
    is_active = models.BooleanField(default=True, verbose_name='comment_is_active')
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name='replies')
    rate = models.CharField(max_length=10, choices=PRODUCT_STARS, blank=True, verbose_name=_('product rate'))

    # Comment Manager
    objects = models.Manager()  # django default manager
    custom_comment_manager = CustomCommentManager()  # our custom manager

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('product_detail_view', args=[self.product.id])


class Customer(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
