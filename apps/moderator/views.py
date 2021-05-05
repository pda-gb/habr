from django.shortcuts import render
from apps.moderator.models import VerifyArticle, BannedUser


def complaints(request):
    title = "Жалобы"
    page_data = {
        'title': title,
    }
    return render(request, "moderator/complaints.html", page_data)


def review_articles(request):
    title = "Статьи на проверку"
    page_data = {
        'title': title,
    }
    return render(request, "moderator/review_articles.html", page_data)


def banned_users(request):
    title = "Заблокированные пользователи"
    banned_users = BannedUser.objects.filter(is_active=True)
    page_data = {
        'title': title,
    }
    return render(request, "moderator/banned_users.html", page_data)
