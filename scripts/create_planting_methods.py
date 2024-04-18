# Define the list of planting method data
from shop.models.planting_method import PlantingMethod

# pip install django-extensions
# python manage.py runscript create_planting_methods

planting_methods_data = [
    {"name": "Direct Sowing", "slug": "direct-sowing", "is_homepage": True, "status": "published", "ordering": 0},
    {"name": "Transplanting", "slug": "transplanting", "is_homepage": True, "status": "published", "ordering": 1},
    {"name": "Container Gardening", "slug": "container-gardening", "is_homepage": True, "status": "published", "ordering": 2},
    {"name": "Raised Bed Gardening", "slug": "raised-bed-gardening", "is_homepage": True, "status": "published", "ordering": 3},
    {"name": "Hydroponics", "slug": "hydroponics", "is_homepage": True, "status": "published", "ordering": 4},
    {"name": "Aquaponics", "slug": "aquaponics", "is_homepage": True, "status": "published", "ordering": 5},
    {"name": "Square Foot Gardening", "slug": "square-foot-gardening", "is_homepage": True, "status": "published", "ordering": 6},
    {"name": "Permaculture", "slug": "permaculture", "is_homepage": True, "status": "published", "ordering": 7},
    {"name": "No-till Gardening", "slug": "no-till-gardening", "is_homepage": True, "status": "published", "ordering": 8},
    {"name": "Lasagna Gardening", "slug": "lasagna-gardening", "is_homepage": True, "status": "published", "ordering": 9},
    # Add more planting method data here
]

# Create PlantingMethod objects from the list of planting method data
planting_methods = [PlantingMethod(**data) for data in planting_methods_data]

# Use bulk_create() to save the PlantingMethod objects in bulk
PlantingMethod.objects.bulk_create(planting_methods)
