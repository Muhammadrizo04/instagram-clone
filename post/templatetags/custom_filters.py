from django import template

register = template.Library()

@register.filter(name='endswith')
def endswith(value, arg):
    """Custom template filter to replicate the 'endswith' method."""
    return value.endswith(arg)
