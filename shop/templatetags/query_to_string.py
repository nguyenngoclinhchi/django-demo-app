from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag
def query_to_string(params, query_add = None, value_add = None):
    # cannot directly modify the params as they will affect the UI
    params_copy = params.copy()
    if query_add and value_add: 
        params_copy[query_add] = value_add
    params_copy = {k: v for k, v in params_copy.items() if v}
    if not params_copy: 
        return ""
    return "?" + urlencode(params_copy)
