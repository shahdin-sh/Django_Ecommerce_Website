from django.db import models
from django.shortcuts import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model


class Product(models.Model):
    product_title = models.CharField(max_length=100)
    product_description = models.TextField()
    product_datetime_created = models.DateTimeField(auto_now_add=True)
    product_datetime_modified = models.DateTimeField(auto_now=True)
    product_price = models.PositiveIntegerField(default=0)
    product_existence = models.BooleanField(default=True)
    product_cover = models.ImageField(upload_to='product/', default='default_product/shop_cart.jpg')

    def __str__(self):
        return self.product_title

    def get_absolute_url(self):
        return reverse('product_detail_view', args=[self.id])


class UserComments(models.Model):
    PRODUCT_STARS = [
        ('1', 'Very bad'),
        ('2', 'Bad'),
        ('3', 'Normal'),
        ('4', 'Good'),
        ('5', 'Perfect'),
    ]
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name='replies')
    rate = models.CharField(max_length=10, choices=PRODUCT_STARS)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('product_detail_view', args=[self.product.id])

