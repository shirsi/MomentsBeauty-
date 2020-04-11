from django.db import models
from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.shortcuts import reverse


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    brand = models.CharField(max_length=200)
    brand_info = models.TextField(blank=True)
    how_to = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    price = models.FloatField()
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    makeup = models.BooleanField(default=True)
    skincare = models.BooleanField(default=False)
    hair = models.BooleanField(default=False)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    is_published = models.BooleanField(default=True)
    slug = models.SlugField()
    size = models.FloatField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:products", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("shop:add-to-cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("shop:remove-from-cart", kwargs={'slug': self.slug})


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def get_total_product_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_product_price()
        return total
