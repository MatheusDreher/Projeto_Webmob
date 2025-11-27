# market/templatetags/market_filters.py

from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Divide a string pelo argumento fornecido.
    Uso: {{ value|split:" " }}
    """
    return value.split(arg)