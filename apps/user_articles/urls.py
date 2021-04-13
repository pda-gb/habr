from django.urls import path

import apps.user_articles.views as user_articles


app_name = 'user_articles'

urlpatterns = [
    path('', user_articles.user_articles, name='user_articles'),
    path('publications/', user_articles.user_articles, name='publications'),
    path('user_articles/', user_articles.user_articles, name='my_articles'),
    path('draft', user_articles.user_articles, name='draft'),
]