from django.urls import path

import apps.account.views as account

app_name = "account"

urlpatterns = [
    path("articles_list/", account.get_articles, name="articles_list"),
    path("add_article/", account.add_article, name="add_article"),
    path("del_article/<int:pk>", account.del_article, name="del_article"),
    path("edit_profile/", account.edit_profile, name="edit_profile"),
]
