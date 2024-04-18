# Define the list of product data
from shop.models import Category, PlantingMethod, Product
from random import randint, choice
from django.db import transaction
from django.utils.text import slugify
from .products import PRODUCTS

# pip install django-extensions
# python manage.py runscript create_products

@transaction.atomic
def add_products():
    # Define plant names for each category
    plant_names_by_category = PRODUCTS
    # Define product data
    products_data = [
        {
            "name": plant_data["name"],
            "slug": slugify(plant_data["name"]),
            "status": "published",
            "ordering": i,
            "special": True if i % 2 == 0 else False,  # Set special to True for even indices
            "price": randint(100000, 200000) * 1000,  # Price ending with "000"
            "price_sale": randint(80000, 150000) * 1000 if i % 3 == 0 else None,  # Random price sale for every third product
            "summary": plant_data["summary"],
            "content": plant_data["content"],
            "image": None,
            "category": Category.objects.get(name=category),
            "planting_methods": [PlantingMethod.objects.get(ordering=randint(0, 9)) for _ in range(randint(1, 5))]  # Random planting methods by ID
        }
        for category, plants_list in plant_names_by_category.items()
        for i, plant_data in enumerate(plants_list, start=1)
    ]

    # Create products without planting_methods
    created_products = [Product.objects.create(**{k: v for k, v in product_data.items() if k != 'planting_methods'}) for product_data in products_data]

    # Associate planting methods with products
    for product, product_data in zip(created_products, products_data):
        product.planting_methods.set([method for method in product_data["planting_methods"]])

# Call the function to add products with associated planting methods
add_products()