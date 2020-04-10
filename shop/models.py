from django.db import models
from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save


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

    def __str__(self):
        return self.title


class OrderProduct(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.title
