from django.urls import path

import apps.articles.views as main_page

app_name = "articles"

urlpatterns = [
    path("", main_page.main_page, name="main_page"),
    path("all/", main_page.main_page, name="all_hubs"),
    path("<int:page>/", main_page.main_page, name="articles_page"),
    path("article/<int:pk>/", main_page.article, name="article"),
    path("hub/<int:pk>/", main_page.hub, name="hub"),
    path("hub/<int:pk>/<int:page>", main_page.hub, name="articles_hub_pag"),
    path("ajax/change_rate/", main_page.change_article_rate, name="ajax_change_rate"),
    path("ajax/rate_author/", main_page.like_dislike_author_ajax, name="ajax_rate_author"),
    path("author/<int:pk>/", main_page.show_author_profile, name="author_profile"),
    path('search/<int:page>/', main_page.search_articles, name='search_articles')
]
