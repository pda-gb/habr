from datetime import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from apps.authorization.models import HabrUser
from apps.moderator.forms import BannedUserForm
from apps.moderator.models import BannedUser, VerifyArticle


def complaints(request):
    title = "Жалобы"
    page_data = {
        'title': title,
    }
    return render(request, "moderator/complaints.html", page_data)


def review_articles(request):
    """получение всех статей на проверку"""
    articles = VerifyArticle.get_all_articles()
    title = "Статьи на проверку"
    page_data = {
        "title": title,
        "articles": articles,
    }
    return render(request, "moderator/review_articles.html", page_data)


def add_user_ban(request, pk):
    title = "Блокирование пользователя"
    current_user = HabrUser.objects.get(pk=pk)

    if request.method == 'POST':
        ban_form = BannedUserForm(request.POST)
        if ban_form.is_valid():
            banned_user_query = BannedUser.objects.filter(offender=pk)
            if banned_user_query:
                banned_user = banned_user_query[0]
                banned_user.is_active = True
                banned_user.reason = request.POST["reason"]
                if request.POST.get("is_forever"):
                    banned_user.is_forever = True
                else:
                    banned_user.is_forever = False
                    banned_user.num_days = request.POST["num_days"]
                banned_user.date_ban = datetime.today()
                banned_user.save()
            else:
                BannedUser.objects.create(offender=current_user,
                                          reason=request.POST["reason"],
                                          num_days=request.POST["num_days"],
                                          is_active=True,
                                          is_forever=True if request.POST.get(
                                              "is_forever") else False)
            return HttpResponseRedirect(reverse("articles:author_profile",
                                                args=[pk]))
        else:
            messages.error(request, 'ошибка')
    else:
        ban_form = BannedUserForm()
    page_data = {
        "title": title,
        "ban_form": ban_form,
        "current_user_pk": pk,
    }
    return render(request, 'moderator/add_ban.html', page_data)


def remove_user_ban(request, pk):
    current_user = BannedUser.objects.get(offender=pk)
    current_user.delete()
    return HttpResponseRedirect(reverse("articles:author_profile", args=[pk]))


def banned_users(request):
    title = "Заблокированные пользователи"
    banned_users_query = BannedUser.objects.filter(is_active=True)
    page_data = {
        "title": title,
        "banned_users": banned_users_query
    }
    return render(request, "moderator/banned_users.html", page_data)

# def get_articles_for_verification(request):
#     """получение всех статей на проверку"""
#     articles = VerifyArticle.get_all_articles()
#     page_data = {
#         "articles": articles,
#     }
#     print(f'{articles=}')
#     return render(request, "moderator/review_articles.html", page_data)
