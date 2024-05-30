from shop.models.blog import Blog
from .blogs import BLOGS

# pip install django-extensions
# python manage.py runscript create_blogs

def run(): 
    # Create Category objects from the list of category data
    # **data: The double asterisk ** is used to unpack the dictionary data. It takes all the key-value pairs in the dictionary data
    # {} -> name:..., slug:..., is_homepage:..., status:...., ordering:... to pass into constructor
    blogs = [Blog(**data) for data in BLOGS]

    # Use bulk_create() to save the Category objects in bulk
    Blog.objects.bulk_create(blogs)
