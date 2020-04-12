from django.contrib import admin
from .models import Product, OrderProduct, Order, UserProfile, FavoritedProduct

admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(UserProfile)
admin.site.register(FavoritedProduct)
