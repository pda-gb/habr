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


from django.urls import path

import apps.authorization.views as auth

app_name = "auth"

urlpatterns = [
    path("login/", auth.login, name="login"),
    path("register/", auth.register, name="register"),
    path("logout/", auth.logout, name="logout"),
    path("edit/", auth.edit, name="edit"),
    path("forgive/", auth.forgive, name="forgive"),
]
