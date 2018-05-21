from django import template
from django.utils.text import slugify

register = template.Library()

@register.simple_tag
def slug_url(value):
        slug = slugify(value)

        return slug