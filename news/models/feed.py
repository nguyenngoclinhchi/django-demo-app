from django.db import models
from django.urls import reverse

from news.helpers import *
from news.define import *

# Create your models here.
class Feed(models.Model):
    class Meta: 
        verbose_name_plural=TABLE_FEED_SHOW

    name = models. CharField(unique=True, max_length=100)
    slug = models. SlugField(unique=True, max_length=100)
    status = models.CharField(max_length=10, choices=APP_VALUE_STATUS_CHOICE, default= 'draft')
    ordering = models.IntegerField(default=0)
    link = models.CharField(max_length=250)

    def __str__(self): # custom notifications in admin page to inform what object is save
        # when saving, it returns to name not object anymore
        return self.name

    def get_absolute_url(self):
        # get the slug from the constructor, not the post_slug
        return reverse("news:feed", kwargs={"feed_slug": self.slug})
