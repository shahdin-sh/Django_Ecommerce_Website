# Generated by Django 4.0.2 on 2022-08-23 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0021_alter_product_product_classification'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_likes',
            field=models.ForeignKey(blank=True, default=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes_on_products', to=settings.AUTH_USER_MODEL),
        ),
    ]
