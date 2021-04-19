from django.urls import path

import apps.articles.views as main_page
import apps.comments.views as comments

app_name = "articles"

urlpatterns = [
    path("", main_page.main_page, name="main_page"),
    path("article/<int:pk>", main_page.article, name="article"),
    path('create-comment/<int:pk>', main_page.create_comment, name='comment_create'),
    path('create-child-comment/<int:pk>', main_page.create_child_comment, name='comment_child_create'),
    path("hub/<int:pk>", main_page.hub, name="hub"),
]
