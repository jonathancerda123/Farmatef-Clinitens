from django import template
from django.utils.safestring import mark_safe
from core.html import sanitizar_html

register = template.Library()


@register.filter
def clinical_html(value):
    return mark_safe(sanitizar_html(value))
