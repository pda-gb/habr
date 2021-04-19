from django.template import Library

register = Library()

@register.filter
def comments_filter(obj):
    print(obj)

