from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Product, OrderProduct, Order
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    # products = Product.objects.order_by(
    #     '-product_date').filter(is_published=True)[:3]
    # context = {
    #     'products': products
    # }
    return render(request, 'shop/index.html')


def product_list(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'shop/product_list.html', context)


def checkout(request):
    return render(request, 'shop/checkout.html')


class MakeupView (ListView):
    model = Product
    paginate_by = 20
    template_name = 'shop/makeup.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'shop/order-summary.html', context)
        except Order.DoesNotExist:
            message.error(self.request, "You don't have order", context)
            return redirect('/')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # print(order)
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            return redirect('shop:products', slug=slug)
        else:
            order.products.add(order_product)
            messages.success(request, "This item was added to your cart.")
    else:
        ordered_date = datetime.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.success(request, "This item was added to your cart.")
    return redirect('shop:products', slug=slug)

    # def makeup(request):
    #     context = {
    #         products: Product.objects.all()
    #     }
    #     return render(request, 'makeup.html')


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    print(product)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        print(order.products)
        if order.products.filter(product__slug=product.slug).exists():
            print('in here')
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            print(order_product)
            order.products.remove(order_product)
            order_product.delete()

        else:
            messages.warning(request, "This product was not in your cart")
            return redirect('shop:products', slug=slug)
    else:
        return redirect('shop:products', slug=slug)
    return redirect('shop:products', slug=slug)


def remove_single_product_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    print(product)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        print(order.products)
        if order.products.filter(product__slug=product.slug).exists():
            print('in here')
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            print(order_product)
            order_product.quantity -= 1
            order_product.save()
            return redirect('shop:order-summary')
        else:
            messages.warning(request, "This product was not in your cart")
            return redirect('shop:order-summary', slug=slug)
    else:
        return redirect('shop:products', slug=slug)
    return redirect('shop:products', slug=slug)


def add_to_single_product_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # print(order)
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            return redirect('shop:order-summary')
        else:
            order.products.add(order_product)
    else:
        ordered_date = datetime.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.success(request, "This item was added to your cart.")
    return redirect('shop:order-summary')
