from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.core.paginator import Paginator


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
    # a dic for context
    dic = {
        'product_detail': product_detail,
    }
    return render(request, 'product/product_detail_view.html', dic)

