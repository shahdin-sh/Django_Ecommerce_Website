# Generated by Django 4.0.2 on 2022-09-10 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_product_product_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_description',
        ),
    ]
