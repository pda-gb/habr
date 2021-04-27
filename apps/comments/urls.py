from django.urls import path

import apps.comments.views as comments

from .apps import CommentsConfig

app_name = CommentsConfig.name

urlpatterns = [
    path("create/<int:pk>", comments.create_comment, name="comment_create"),
    path("create-child/<int:pk>", comments.create_child_comment, name="comment_child_create"),
    path("ajax/like", comments.like_dislike_ajax, name="ajax_comment"),
]
