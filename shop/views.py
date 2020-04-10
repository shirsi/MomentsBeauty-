from django.shortcuts import render
from .models import Product


def index(request):
    products = Product.objects.order_by(
        '-list_date').filter(is_published=True)[:3]
    context = {
        'products': products
    }
    return render(request, 'index.html')


def product_list(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'shop/product_list.html', context)


def checkout(request):
    return render(request, 'shop/checkout.html')
