from django.utils import timezone
from django.db import models
from django.urls import reverse
from shop.custom_field import CustomBooleanFieldContact
from shop.define import *

# Create your models here.

class Contact(models.Model):
    class Meta: 
        verbose_name_plural=TABLE_CONTACT_SHOW
    # no need to be unique
    name = models.CharField(max_length=100, verbose_name="Name of Contact")
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    contacted = CustomBooleanFieldContact()
    message_admin = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self): # custom notifications in admin page to inform what object is save
        # when saving, it returns to name not object anymore
        return self.name

    def get_absolute_url(self):
        # get the slug from the constructor, not the post_slug
        return reverse("shop:contact", kwargs={"contact_slug": self.slug})