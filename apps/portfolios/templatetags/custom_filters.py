import json
from django import template

register = template.Library()


@register.filter(name="multiply_int")
def multiply_int(value, arg):
    """Multiplies the value by the arg."""
    return int(value) * int(arg)


@register.filter(name="json_dumps")
def json_dumps(value):
    """Multiplies the value by the arg."""
    return json.dumps(value)
