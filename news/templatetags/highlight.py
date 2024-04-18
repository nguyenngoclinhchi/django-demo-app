from re import IGNORECASE, compile, escape
from django.utils.safestring import mark_safe

from django import template

register = template.Library()

def highlight(text, keyword):
    rgx = compile(escape(keyword), IGNORECASE)
    return mark_safe(
        rgx.sub(
            lambda m: '<span class="highlight">{}</span>'.format(m.group()),
            text
        )
    )
register.filter('highlight', highlight)
