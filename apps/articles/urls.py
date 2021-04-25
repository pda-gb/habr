from django.urls import path

import apps.articles.views as main_page

app_name = "articles"

urlpatterns = [
    path("", main_page.main_page, name="main_page"),
    path("<int:page>/", main_page.main_page, name="articles_page"),
    path("article/<int:pk>", main_page.article, name="article"),
    path("hub/<int:pk>", main_page.hub, name="hub"),
    path("ajax/change_rate", main_page.change_article_rate, name="ajax_change_rate"),
    path("author/<int:pk>", main_page.show_author_profile, name="author_profile"),
    path('search/', main_page.SearchArticlesView.as_view(), name='search_articles')
]
