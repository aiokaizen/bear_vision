from django import template

register = template.Library()


@register.filter(name="get_field_value")
def get_field_value(obj, field):
    if isinstance(field, tuple):
        field = field[0]

    if hasattr(obj, field.name):
        attr = getattr(obj, field.name, "-----")
        if callable(attr):
            print("callable:", attr)
            return attr()
        return attr
    return "-----"
