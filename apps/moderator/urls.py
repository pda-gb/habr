from django.urls import path

import apps.moderator.views as moderator

app_name = "moderator"

urlpatterns = [
    path("complaints/", moderator.complaints, name="complaints"),
    path("review_articles/", moderator.review_articles, name='review_articles'),
    path("banned_users/", moderator.banned_users, name='banned_users'),
    path("add_user_ban/<int:pk>", moderator.add_user_ban, name='add_user_ban'),
    path("remove_user_ban/<int:pk>", moderator.remove_user_ban, name='remove_user_ban'),
]