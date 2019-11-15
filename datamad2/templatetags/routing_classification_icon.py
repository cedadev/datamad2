from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def icon(value):
    if value == "Marine":
        return mark_safe("<a id='science-icon' title='Marine' data-toggle='tooltip'><i class='fa "
                         "fa-fish fa-lg' "
                         "style='color:#79e2e8'></i></a>")

    elif value == "Earth":
        return mark_safe("<a id='science-icon' title='Earth' data-toggle='tooltip'><i class='fa "
                         "fa-seedling fa-lg' "
                         "style='color:#9ce879'></i></a>")

    elif value == "Atmospheric":
        return mark_safe("<a id='science-icon' title='Atmospheric' data-toggle='tooltip'><i "
                         "class='fa fa-cloud fa-lg' "
                         "style='color:#a9c3c7'></i></a>")

    elif value == "Freshwater":
        return mark_safe("<a id='science-icon' title='Freshwater' data-toggle='tooltip'><i "
                         "class='fa fa-water fa-lg' "
                         "style='color:#81aae3'></i></a>")

    elif value == "Terrestrial":
        return mark_safe("<a id='science-icon' title='Terrestrial' data-toggle='tooltip'><i "
                         "class='fa "
                         "fa-globe-americas fa-lg' style='color:#ba9b72'></i></a>")

    else:
        return mark_safe("<a id='science-icon' title='None' data-toggle='tooltip'><i class='fa "
                         "fa-times-circle fa-lg'></i></a>")
