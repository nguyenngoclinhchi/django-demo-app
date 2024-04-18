from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField

from .planting_method import PlantingMethod
from .category import Category
from shop.custom_field import CustomBooleanField
from shop.helpers import *
from shop.define import *

# Create your models here.
class Product(models.Model):
    class Meta: 
        verbose_name_plural=TABLE_PRODUCT_SHOW

    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    status = models.CharField(max_length=10, choices=APP_VALUE_STATUS_CHOICE, default='draft')
    ordering = models. IntegerField(default=0)
    special = CustomBooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=0) # give us decimal numbers: 10 digit with 0 decimal place
    price_sale = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True) # sale price
    price_real = models.DecimalField(max_digits=10, decimal_places=0, editable=False) # hide from the admin page, cannot be edited
    total_sold = models.IntegerField(default=0, editable=False)
    summary = models.TextField()
    content = HTMLField()
    image = models.ImageField(
        upload_to=get_file_path, 
        blank=True,
        null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    planting_methods = models.ManyToManyField(PlantingMethod) # many-to-many relationships
    
    def __str__(self): # custom notifications in admin page to inform what object is save
        # when saving, it returns to name not object anymore
        return self.name
    
    def get_absolute_url(self):
        # get the slug from the constructor, not the post_slug
        return reverse("shop:product", kwargs={"product_slug": self.slug, "product_id": self.id})
    
    # override the save method
    def save(self, *args, **kwargs): 
        self.price_real = self.price_sale if self.price_sale else self.price
        super().save(*args, **kwargs)