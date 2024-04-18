from bulk_update.helper import bulk_update
from shop.models.product import Product

# python manage.py runscript update_products

products = Product.objects.all()

for item in products:
    item.price = item.price/100
    item.price_real = item.price_real/100
    item.price_sale = item.price_sale/100 if item.price_sale else None

bulk_update(products) # updates all columns using the default db