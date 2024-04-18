from re import IGNORECASE, compile, escape
from django.utils.safestring import mark_safe

from django import template

register = template.Library()

def highlight_shop(text, keyword):
    if not keyword:
        return text
    rgx = compile(escape(keyword), IGNORECASE)
    return mark_safe(
        rgx.sub(
            lambda m: '<span class="highlight">{}</span>'.format(m.group()),
            text
        )
    )
register.filter('highlight_shop', highlight_shop)
