from django.urls import path

import apps.comments.views as comments

from .apps import CommentsConfig

app_name = CommentsConfig.name

urlpatterns = [
    #path('', comments.comments, name='view'),
]