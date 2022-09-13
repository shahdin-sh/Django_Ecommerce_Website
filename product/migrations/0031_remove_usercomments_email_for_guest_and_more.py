# Generated by Django 4.0.2 on 2022-09-10 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0030_usercomments_email_for_guest_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercomments',
            name='email_for_guest',
        ),
        migrations.RemoveField(
            model_name='usercomments',
            name='name_for_guest',
        ),
        migrations.AlterField(
            model_name='usercomments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
