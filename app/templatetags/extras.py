from django import template
register= template.Library()

def replace(value):
    return value.replace(' ','-')