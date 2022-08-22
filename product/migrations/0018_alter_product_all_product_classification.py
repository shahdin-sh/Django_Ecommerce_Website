# Generated by Django 4.0.2 on 2022-08-22 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_product_all_product_classification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='all_product_classification',
            field=models.CharField(choices=[('CAF', 'Clothing and fashion'), ('SS', 'Supermarket Items'), ('HA', 'Home Appliances'), ('T', 'Toys'), ('B', 'Books'), ('Un', 'Uncategorized')], default=('SS', 'Supermarket Items'), max_length=200),
        ),
    ]