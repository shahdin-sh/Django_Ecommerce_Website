# Generated by Django 4.0.2 on 2022-08-13 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_usercomments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercomments',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='product.product'),
        ),
    ]
