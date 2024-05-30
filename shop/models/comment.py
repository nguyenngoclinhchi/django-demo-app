from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
# from .blog import Blog
from shop.define import *


class Comment(models.Model):
  class Meta: 
    verbose_name_plural=TABLE_COMMENT_SHOW

  # Define a ForeignKey to ContentType to dynamically associate with any model
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  # Store the ID of the related object
  object_id = models.PositiveIntegerField()
  # Use GenericForeignKey to create dynamic relationships
  content_object = GenericForeignKey('content_type', 'object_id')
  # Other fields
  text = models.TextField()

# Usage
# blog = Blog.objects.get(pk=1)
# comment = Comment(content_object=blog, text="Great blog!")
# comment.save()  