from django.db import models
from django.urls import reverse

from news.custom_field import CustomBooleanField
from news.helpers import *
from news.define import *

# Create your models here.

class Category(models.Model):
    class Meta: 
        verbose_name_plural=TABLE_CATEGORY_SHOW
    
    name = models.CharField(unique=True, max_length=100, verbose_name="Name of Category")
    slug = models.SlugField(unique=True, max_length=100)
    is_homepage = CustomBooleanField()
    layout = models.CharField(max_length=10, choices=APP_VALUE_LAYOUT_CHOICE, default=APP_VALUE_LAYOUT_DEFAULT)
    status = models.CharField(max_length=10, choices=APP_VALUE_STATUS_CHOICE, default=APP_VALUE_STATUS_DEFAULT)
    ordering = models. IntegerField(default=0)

    # name you want to change into admin page (Categorys --> Category)

    def __str__(self): # custom notifications in admin page to inform what object is save
        # when saving, it returns to name not object anymore
        return self.name

    def get_absolute_url(self):
        # get the slug from the constructor, not the post_slug
        return reverse("news:category", kwargs={"category_slug": self.slug})