from django.template.loader import render_to_string
from django import template

register = template.Library()

@register.simple_tag
def render_share_shop(src_template, items, keyword=None):
    # render the template
    return render_to_string(
        'shop/pages/share/' + src_template, 
        { 
            "items": items,
            "keyword": keyword
        }
    )
