from django import template
from django.template.defaultfilters import stringfilter
register= template.Library()

#@register.simple_tag
def cut(value, arg):
    return value.upper()
@register.filter
@stringfilter    
def lower(value):
    return value.lower()    

register.filter('lower', lower)
register.filter('cut',cut)    