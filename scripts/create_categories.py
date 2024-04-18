from shop.models.category import Category

# pip install django-extensions
# python manage.py runscript create_categories

def run(): 
    categories_data = [
        {"name": "Indoor Plants", "slug": "indoor-plants", "is_homepage": True, "status": "published", "ordering": 0},
        {"name": "Outdoor Plants", "slug": "outdoor-plants", "is_homepage": True, "status": "published", "ordering": 1},
        {"name": "Succulents", "slug": "succulents", "is_homepage": True, "status": "published", "ordering": 2},
        {"name": "Cacti", "slug": "cacti", "is_homepage": True, "status": "published", "ordering": 3},
        {"name": "Flowering Plants", "slug": "flowering-plants", "is_homepage": True, "status": "published", "ordering": 4},
        {"name": "Herbs", "slug": "herbs", "is_homepage": True, "status": "published", "ordering": 5},
    ]

    # Create Category objects from the list of category data
    categories = [Category(**data) for data in categories_data]

    # Use bulk_create() to save the Category objects in bulk
    Category.objects.bulk_create(categories)
