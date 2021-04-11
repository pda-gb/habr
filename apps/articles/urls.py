from django.urls import path

import apps.articles.views as main_page

app_name = "articles"

urlpatterns = [
    path("", main_page.main_page, name="main_page"),
    path("article/<int:pk>", main_page.article, name="article"),
    path("hub/<int:pk>", main_page.hub, name="hub"),
]