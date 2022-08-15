from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, UserComments
from django.core.paginator import Paginator
from .forms import UserCommentsForm
from django.contrib.auth import get_user_model


def products_list_view(request):
    products = Product.objects.all().filter(product_existence=True).order_by('-product_datetime_created')
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # context
    dic = {
        'products': page_obj,
    }
    # rendering our object
    return render(request, 'product/products_list_view.html', dic)


def product_detail_view(request, pk):
    products = Product.objects.all().filter(product_existence=True)
    product_detail = get_object_or_404(products, pk=pk)
    comments = UserComments.objects.all().filter(is_active=True, parent__isnull=True)
    # comment section for user started
    if request.method == 'POST':
        comment_form = UserCommentsForm(request.POST)

        if comment_form.is_valid():
            # Replay section
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except TypeError:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = UserComments.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj
            # End of replay section
            new_comment = comment_form.save(commit=False)
            new_comment.product = product_detail
            new_comment.user = request.user
            new_comment.save()
            comment_form = UserCommentsForm()
    else:
        comment_form = UserCommentsForm()
    # end of comment section
    # a dic for context
    dic = {
        'product_detail': product_detail,
        'comment_form': comment_form,
        'comments': comments
    }
    return render(request, 'product/product_detail_view.html', dic)


def edit_user_comments(request, pk, comment_id):
    user = request.user
    user_comments = user.comments.filter(is_active=True, parent__isnull=True)
    getting_particular_user_comment = get_object_or_404(user_comments, pk=comment_id)
    edit_comment_form = UserCommentsForm(request.POST, instance=getting_particular_user_comment)
    if edit_comment_form.is_valid():
        edit_comment_form.save()
        edit_comment_form = UserCommentsForm()
        redirect('post_detail_view', pk=pk)
    # dic for context
    dic = {
        'edit_comment_form': edit_comment_form,
    }
    return render(request, 'product/edit_product_comments.html', dic)
