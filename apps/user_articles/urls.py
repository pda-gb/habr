import apps.articles.views as main_page
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import apps.user_articles.views as pub

app_name = 'user_articles'

urlpatterns = [
    path('publications/', pub.publications, name='publications'),
    path('user_articles/', pub.user_articles, name='my_articles'),
    path('draft', pub.draft, name='draft'),
]