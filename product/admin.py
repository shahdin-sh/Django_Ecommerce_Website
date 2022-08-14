from django.contrib import admin
from .models import Product, UserComments


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_title', 'product_datetime_created', 'product_price', 'product_existence', 'product_cover', 'comments']

    def comments(self, obj):
        if obj.comments.exists():
            return len(obj.comments.all().filter(is_active=True))
        return '0'


class ProductCommentsAdmin(admin.ModelAdmin):
    list_display = ['text', 'datetime_created', 'is_active', 'parent', 'rate', 'product']


# registering our models ------> first register model then register admin

admin.site.register(Product, ProductAdmin)
admin.site.register(UserComments, ProductCommentsAdmin)
