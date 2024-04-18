from django.db import models
from django.urls import reverse
from django.utils import timezone
from shop.define import *

# Create your models here.

class Order(models.Model):
    class Meta: 
        verbose_name_plural=TABLE_ORDER_SHOW
    
    name = models.CharField(max_length=100, verbose_name="Name of Order")
    code = models.CharField(unique=True, max_length=20)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    status = models.CharField(
        max_length=20, 
        choices=APP_VALUE_ORDER_STATUS_CHOICE, 
        default=APP_VALUE_ORDER_STATUS_DEFAULT)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self): # custom notifications in admin page to inform what object is save
        # when saving, it returns to name not object anymore
        return self.name

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.__important_fields = ['status']
        for field in self.__important_fields:
            setattr(self, '__original_%s' % field, getattr(self, field))

    def has_changed_status(self):
        for field in self.__important_fields:
            orig = '__original_%s' % field
            if getattr(self, orig) != getattr(self, field):
                return True
        return False

    def update_total_sold(self):
        # check if status is finish, iterate through all order items to update total_sold
        if self.status == APP_VALUE_ORDER_STATUS_FINISH:
            if self.has_changed_status(): # status change or remain
                for item in self.orderitem_set.all():
                    product = item.product
                    product.total_sold += item.quantity
                    product.save()
