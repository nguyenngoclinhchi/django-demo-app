from django.utils import timezone
import requests

from .helpers import *
from .define import *
from .models import *
from django.db.models import Count
import json

def items_category_menu(request): 
    items_category_menu = Category.objects.filter(
        status=APP_VALUE_STATUS_ACTIVE).order_by('ordering')[:SETTINGS_CATEGORIES_TOTAL_MENU]
    return {
        "items_category_menu": items_category_menu
    }

def item_cart_info_menu(request):
    cart = request.session.get("cart", {})
    total_cart = 0
    quantity_cart = 0
    for product_id, quantity in cart.items(): 
        product = Product.objects.get(id=product_id)
        price = product.price_real
        total = price*quantity
        total_cart += total
        quantity_cart += quantity
    return {
        "item_cart_info_menu": {
            "total_cart": total_cart,
            "quantity_cart": quantity_cart
        }
    }