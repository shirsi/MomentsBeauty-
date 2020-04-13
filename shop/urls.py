from django.urls import path
from . import views
from .views import (ProductDetailView,
                    add_to_cart, remove_from_cart, OrderSummaryView, remove_single_product_from_cart, add_to_single_product_cart, remove_product_from_cart, add_to_favorites, remove_from_favorites, UserProfileView, index)

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('products/', views.product_list, name='products'),
    path('checkout/', views.checkout, name='checkout'),
    path('hair/', views.hair, name='hair'),
    path('makeup/', views.makeup, name='makeup'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('dashboard/', UserProfileView.as_view(), name='dashboard'),
    path('products/<slug>/', ProductDetailView.as_view(), name='products'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-to-favorites/<slug>/', add_to_favorites, name='add-to-favorites'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-from-favorites/<slug>/',
         remove_from_favorites, name='remove-from-favorites'),
    path('remove-single-product-from-cart/<slug>/',
         remove_single_product_from_cart, name='remove-single-product-from-cart'),
    path('add-to-single-product-cart/<slug>/',
         add_to_single_product_cart, name='add-to-single-product-cart'),
    path('remove-product-from-cart/<slug>/',
         remove_product_from_cart, name='remove-product-from-cart'),
    re_path(r'^.*$', index)


]
app_name = 'shop'
