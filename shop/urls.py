from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.product_list, name='products'),
    path('checkout/', views.checkout, name='checkout'),

]
