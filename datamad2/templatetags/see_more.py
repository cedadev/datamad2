from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def read_more(s, show_words, autoescape=True):
    """Split text after so many words, inserting a "more" link at the end.

    Relies on JavaScript to react to the link being clicked and on classes
    found in Bootstrap to hide elements.
    """
    show_words = int(show_words)
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    words = esc(s).split()

    if len(words) <= show_words:
        return s

    insertion = (
        # The see more link...
        '<span class="read-more">&hellip;'
        '    <a href="#">'
        '        <i class="fa fa-plus-square gray" title="Show All"></i>'
        '    </a>'
        '</span>'
        # The call to hide the rest...
        '<span class="more d-none">'
    )

    # wrap the more part
    words.insert(show_words, insertion)
    words.append('<a href="#">'
                 '<i class="fa fa-minus-square gray" title="Show Less"></i>'
                 '</a> </span>')
    return mark_safe(' '.join(words))

