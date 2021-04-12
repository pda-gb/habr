"""habr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


import apps.articles.views as main_page
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import apps.my_articles.views as pub

app_name = 'pub'

urlpatterns = [
    path('publications/', pub.publications, name='publications'),
    path('my_articles/', pub.my_articles, name='my_articles'),
    path('draft', pub.draft, name='draft'),
]
