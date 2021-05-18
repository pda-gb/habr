from django.urls import path

import apps.moderator.views as moderator

app_name = "moderator"

urlpatterns = [
    path("complaints/", moderator.complaints, name="complaints"),
    path("review_articles/", moderator.review_articles, name='review_articles'),
    path("banned_users/", moderator.banned_users, name='banned_users'),
    path("add_user_ban/<int:pk>/", moderator.add_user_ban, name='add_user_ban'),
    path("remove_user_ban/<int:pk>/", moderator.remove_user_ban, name='remove_user_ban'),
    path("allow_publishing/<int:pk>/", moderator.allow_publishing, name='allow_publishing'),
    path("reject_publishing/<int:pk>/", moderator.reject_publishing, name='reject_publishing'),
    path("return_article/<int:pk>/", moderator.return_article, name='return_article'),
    path("complain_to_article/<int:pk>/", moderator.complain_to_article, name='complain_to_article'),
    path("complain_to_comment/<int:pk>/", moderator.complain_to_comment, name='complain_to_comment'),
    path("send_complain_to_article/<int:pk>/", moderator.send_complain_to_article, name='send_complain_to_article'),
    path("send_complain_to_comment/<int:pk>/", moderator.send_complain_to_comment, name='send_complain_to_comment'),
]