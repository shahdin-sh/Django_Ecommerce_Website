from django.contrib import admin
from .models import Product, UserComments


class ProductCommentsInline(admin.StackedInline):
    model = UserComments
    fields = ['user', 'text', 'is_active', 'parent', 'rate']

    # showing only comments for each product not their replies!!!
    def get_queryset(self, request):
        return self.model.custom_comment_manager

    extra = 0


class CommentsReplayInline(admin.StackedInline):
    model = UserComments

    # showing replay for each comment
    def get_queryset(self, request):
        return self.model.objects.filter(parent__isnull=False, is_active=True)

    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_title', 'product_datetime_created', 'product_price', 'product_existence', 'product_cover', 'comments']

    def comments(self, obj):
        if obj.comments.exists():
            return len(obj.comments.all().filter(is_active=True, parent__isnull=True))
        return '0'

    inlines = [
        ProductCommentsInline,
    ]


class ProductCommentsAdmin(admin.ModelAdmin):
    list_display = ['replay_or_comment', 'user', 'text', 'datetime_created', 'is_active', 'parent', 'rate', 'product']

    def replay_or_comment(self, obj):
        if not obj.parent:
            # when a comment does not have a parent it means that comment is a comment.
            return 'COMMENT'
        else:
            # it means that comment is a child of another comment and has a parent.
            return 'REPLAY'
    inlines = [
        CommentsReplayInline,
    ]

# registering our models ------> first register model then register admin

admin.site.register(Product, ProductAdmin)
admin.site.register(UserComments, ProductCommentsAdmin)
