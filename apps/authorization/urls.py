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
