from django import template
from django.utils.html import mark_safe

from shop.define import *

register = template.Library()

@register.simple_tag
def check_and_show_active_status(real_status, message_status): 
    if message_status == APP_VALUE_ORDER_STATUS_DEFAULT: 
        return "active"
    if message_status == APP_VALUE_ORDER_STATUS_CONFIRM:
        return "active" if (real_status != APP_VALUE_ORDER_STATUS_DEFAULT) else ""
    elif message_status == APP_VALUE_ORDER_STATUS_DELIVERY:
        return "active" if (real_status != APP_VALUE_ORDER_STATUS_DEFAULT and real_status != APP_VALUE_ORDER_STATUS_CONFIRM) else ""
    elif message_status == APP_VALUE_ORDER_STATUS_FINISH: 
        return "active" if (real_status == APP_VALUE_ORDER_STATUS_FINISH) else ""
