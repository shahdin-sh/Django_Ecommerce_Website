from django.db import models
from django.shortcuts import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    product_title = models.CharField(max_length=100, verbose_name='title')
    product_description = models.TextField(verbose_name='description')
    product_datetime_created = models.DateTimeField(auto_now_add=True, verbose_name='datetime_created')
    product_datetime_modified = models.DateTimeField(auto_now=True, verbose_name='datetime_modified')
    product_price = models.PositiveIntegerField(default=0, verbose_name='price')
    product_existence = models.BooleanField(default=True, verbose_name='existence')
    product_cover = models.ImageField(upload_to='product/', default='default_product/shop_cart.jpg', verbose_name='cover')

    def __str__(self):
        return self.product_title

    def get_absolute_url(self):
        return reverse('product_detail_view', args=[self.id])


class CustomCommentManager(models.Manager):
    def get_queryset(self):
        return super(CustomCommentManager, self).get_queryset().filter(is_active=True, parent__isnull=True)


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

