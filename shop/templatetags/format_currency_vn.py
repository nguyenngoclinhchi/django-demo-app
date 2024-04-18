import locale
from re import IGNORECASE, compile, escape
from django.utils.safestring import mark_safe

from django import template

register = template.Library()

def format_currency_vn(number): 
    number = int(float(number))
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    formatted_number = locale.format_string("%d", number, grouping=True) + " VND"
    return formatted_number
register.filter('format_currency_vn', format_currency_vn)
