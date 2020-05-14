from django import template
register = template.Library()

@register.filter
def type(documents):
    return things.filter(category=category)