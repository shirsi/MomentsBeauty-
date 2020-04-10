from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Product, OrderProduct, Order
from datetime import datetime


def index(request):
    products = Product.objects.order_by(
        '-product_date').filter(is_published=True)[:3]
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


class MakeupView (ListView):
    model = Product
    template_name = 'shop/makeup.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = Order.objects.get_or_create(

        product=product

    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
        else:
            order.products.add(order_product)
    else:
        ordered_date = datetime.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)

    return redirect('shop:products', slug=slug)

    # def makeup(request):
    #     context = {
    #         products: Product.objects.all()
    #     }
    #     return render(request, 'makeup.html')


def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                user=request.user,
                orderd=False,
                product=product,

            )[0]
            order.products.remove(order_product)
        else:
            return redirect('shop:products', slug=slug)
    else:
        return redirect('shop:products', slug=slug)
    return redirect('shop:products', slug=slug)
