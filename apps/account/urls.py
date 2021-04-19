from django.urls import path

import apps.account.views as account

app_name = "account"

urlpatterns = [
    path('', account.read_profile, name='read_profile'),
    path('articles/', account.user_articles, name='user_articles'),
    path("add_article/", account.add_article, name="add_article"),
    path("draft_article/<int:pk>", account.draft_article, name="draft_article"),
    path("del_article/<int:pk>", account.del_article, name="del_article"),
    path("edit_profile/", account.edit_profile, name="edit_profile"),
    path('publications/', account.publications, name='publications'),
    path('user_articles/', account.user_articles, name='user_articles'),
    path('draft', account.draft, name='draft'),
    path("edit_profile/edit_password/", account.edit_password, name="edit_password"),
    path("edit_article/<int:pk>", account.edit_article, name="edit_article"),
]
