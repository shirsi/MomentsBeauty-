from django.urls import path
from . import views
from .views import (MakeupView, ProductDetailView,
                    add_to_cart, remove_from_cart, OrderSummaryView, remove_single_product_from_cart, add_to_single_product_cart)

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='products'),
    path('checkout/', views.checkout, name='checkout'),
    path('makeup/', MakeupView.as_view(), name='makeup'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('products/<slug>/', ProductDetailView.as_view(), name='products'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-product-from-cart/<slug>/',
         remove_single_product_from_cart, name='remove-single-product-from-cart'),
    path('add-to-single-product-cart/<slug>/',
         add_to_single_product_cart, name='add-to-single-product-cart')


]
app_name = 'shop'
