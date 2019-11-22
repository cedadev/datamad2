from django import template

register = template.Library()


@register.filter
def lead(value):
    if value.lead_grant == True:
        return True
