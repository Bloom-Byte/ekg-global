from django import template

register = template.Library()


@register.filter(name='multiply_int')
def multiply_int(value, arg):
    """Multiplies the value by the arg."""
    return int(value) * int(arg)
