from django.conf import settings
from django import template


register = template.Library()


@register.filter(name="media_folder_users")
def media_folder_users(string):
    string = str(string)
    if string.startswith("http"):
        return string
    if not string:
        return f"{settings.STATIC_URL}default/default_ava.jpg"
    return f"{settings.MEDIA_URL}{string}"


@register.filter(name="media_folder_images")
def media_folder_images(string):
    string = str(string)
    if string.startswith("http"):
        return string
    elif not string:
        return f"{settings.STATIC_URL}default/default_img_art.jpg"
    return f"{settings.MEDIA_URL}{string}"


@register.filter(name="no_data_specified")
def no_data_specified(string):
    if not string:
        string = "не указано"
    return string
