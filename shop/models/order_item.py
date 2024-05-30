from django.db import models
from django.urls import reverse
from .product import Product
from .order import Order
from shop.define import *

# Create your models here.


class OrderItem(models.Model):
    class Meta:
        verbose_name_plural = TABLE_ORDER_ITEM_SHOW

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    total = models.DecimalField(max_digits=10, decimal_places=0)

    def get_absolute_url(self):
        # get the category links from the app named 'shop'
        return reverse("shop:category", kwargs={"category_slug": self.slug})

    def __str__(self):
        return ""
