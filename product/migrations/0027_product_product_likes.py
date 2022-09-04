# Generated by Django 4.0.2 on 2022-09-03 11:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0026_remove_product_product_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='likes_on_products', to=settings.AUTH_USER_MODEL, verbose_name='likes_on_product'),
        ),
    ]