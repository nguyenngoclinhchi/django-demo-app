from django import template
from shop.helpers import get_currency_vn

register = template.Library()

@register.simple_tag
def get_price_old(price, price_sale):
    # render the template
    return get_currency_vn(price) if price_sale else ""
