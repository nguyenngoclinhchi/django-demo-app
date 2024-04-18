from django.template.loader import render_to_string
from django import template

register = template.Library()

@register.simple_tag
def render_share(src_template, item):
    # render the template
    return render_to_string(
        'pages/share/' + src_template, 
        {"item": item}
    )

register.filter('render_share', render_share)
