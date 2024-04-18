from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField
from news.custom_field import CustomBooleanField
from news.helpers import *
from news.define import *
from .category import Category

# Create your models here.
User = get_user_model()

class Article(models.Model):
    class Meta: 
        verbose_name_plural=TABLE_ARTICLE_SHOW

    name = models.CharField(unique=True, max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    slug = models.SlugField(unique=True, max_length=100)
    status = models.CharField(max_length=10, choices=APP_VALUE_STATUS_CHOICE, default='draft')
    ordering = models. IntegerField(default=0)
    special = CustomBooleanField()
    content = HTMLField()
    image = models.ImageField(
        upload_to=get_file_path, 
        blank=True,
        null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField()

    def __str__(self): # custom notifications in admin page to inform what object is save
        # when saving, it returns to name not object anymore
        return self.name
    
    def get_absolute_url(self):
        # get the slug from the constructor, not the post_slug
        return reverse("news:post", kwargs={"post_slug": self.slug, "post_id": self.id})
    