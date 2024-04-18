from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField

from shop.custom_field import CustomBooleanField
from shop.helpers import *
from shop.define import *

# Create your models here.
class Blog(models.Model):
    class Meta: 
        verbose_name_plural=TABLE_BLOG_SHOW

    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    status = models.CharField(max_length=10, choices=APP_VALUE_STATUS_CHOICE, default='draft')
    ordering = models. IntegerField(default=0)
    special = CustomBooleanField()
    publish_date = models.DateTimeField()
    content = HTMLField()
    image = models.ImageField(
        upload_to=get_file_path, 
        blank=True,
        null=True)
    
    def __str__(self): # custom notifications in admin page to inform what object is save
        # when saving, it returns to name not object anymore
        return self.name
    
    def get_absolute_url(self):
        # get the slug from the constructor, not the post_slug
        return reverse("shop:blog", kwargs={"blog_slug": self.slug, "blog_id": self.id})