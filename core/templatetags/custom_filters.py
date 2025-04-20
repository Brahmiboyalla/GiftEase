from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Returns the value from a dictionary for a given key."""
    return dictionary.get(key, 5)  # Default margin is 5% if brand not found

@register.filter
def mul(value, arg):
    """Multiply two values."""
    return Decimal(value) * Decimal(arg)

@register.filter
def div(value, arg):
    """Divide two values."""
    return Decimal(value) / Decimal(arg)
