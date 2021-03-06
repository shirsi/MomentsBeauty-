from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Product, OrderProduct, Order, UserProfile, FavoritedProduct
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.postgres.search import SearchVector


def home(request):
    products = Product.objects.order_by(
        '-list_date').filter(is_published=True)[:3]
    context = {
        'products': products
    }
    return render(request, 'shop/home.html', context)


def product_list(request):
    products = Product.objects.filter(skincare=True)
    context = {
        'products': products
    }
    return render(request, 'shop/product_list.html', context)


def checkout(request):
    return render(request, 'shop/checkout.html')


def makeup(request):
    products = Product.objects.filter(makeup=True)
    context = {
        'products': products
    }
    return render(request, 'shop/makeup.html', context)


def hair(request):
    products = Product.objects.filter(hair=True)
    context = {
        'products': products
    }
    return render(request, 'shop/hair.html', context)


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


def search(request):
    queryset_list = Product.objects.order_by('-list_date')
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = Product.objects.annotate(
                search=SearchVector(
                    'title') + SearchVector('brand')
            ).filter(search=keywords)
    context = {
        'products': queryset_list

    }
    return render(request, 'shop/search.html', context)


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
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
                order_product.delete()

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


def remove_product_from_cart(request, slug):
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
            return redirect('shop:order-summary')

        else:
            messages.warning(request, "This product was not in your cart")
            return redirect('shop:order-summary')
    else:
        return redirect('shop:products')
    return redirect('shop:products')


################################################################


@login_required
def remove_from_favorites(request, slug):
    product = get_object_or_404(Product, slug=slug)
    print(product)
    favor_qs = UserProfile.objects.filter(user=request.user)

    if favor_qs.exists():
        favor = favor_qs[0]

        print(favor.products)
        if favor.products.filter(product__slug=product.slug).exists():
            print('in here')
            favor_product = FavoritedProduct.objects.filter(
                product=product,
                user=request.user,

            )[0]
            print(favor_product)
            favor.products.remove(favor_product)
            favor_product.delete()
            messages.warning(
                request, "This product was removed from your favorites")
            return redirect('shop:dashboard')
        else:
            messages.warning(request, "This product was not in your favorites")
            return redirect('shop:products', slug=slug)
    else:
        return redirect('shop:products', slug=slug)
        essages.warning(request, "You don't have favorites")
    return redirect('shop:products', slug=slug)


@login_required
def add_to_favorites(request, slug):
    print('favor')
    product = get_object_or_404(Product, slug=slug)
    favor_product, created = FavoritedProduct.objects.get_or_create(
        product=product,
        user=request.user,
    )
    favor_qs = UserProfile.objects.filter(user=request.user)
    print(favor_qs)
    if favor_qs.exists():
        favor = favor_qs[0]

        if favor.products.filter(product__slug=product.slug).exists():

            messages.success(
                request, "This product already in your favorites.")
        else:
            favor.products.add(favor_product)
            messages.success(
                request, "This product was added to your favorites.")
    else:
        favor = UserProfile.objects.create(
            user=request.user)
        favor.products.add(favor_product)
        messages.success(request, "This product was added to your favorites.")

    return redirect('shop:products', slug=slug)


class UserProfileView(LoginRequiredMixin, View):
    print('hi')

    def get(self, *args, **kwargs):
        print('here')
        try:
            favor = UserProfile.objects.get(
                user=self.request.user)
            print(favor)
            context = {
                'object': favor
            }
            for product in favor.products.all():
                print(product)

            return render(self.request, 'accounts/dashboard.html', context)
        except UserProfile.DoesNotExist:
            message.error(self.request, "You don't have favorites", context)
            return render('accounts/dashboard.html')


# def favorites_list(request):
#     favor = UserProfile.objects.all()
#     for product in favor.products.all():
#         print(product)
#     context = {
#         'object': favor
#     }
#     return render(request, 'accounts/dashboard.html', context)
