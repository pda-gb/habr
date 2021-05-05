from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from apps.moderator.forms import BannedUserForm
from apps.moderator.models import VerifyArticle, BannedUser
from apps.authorization.models import HabrUser


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


def add_user_ban(request, pk):
    title = 'Блокирование пользователя'
    current_user = HabrUser.objects.get(pk=pk)
    print(f'REQUEST: {request.POST}')

    if request.method == 'POST':
        print(f'1111111: {request.POST["reason"]}')
        print(f'22222: {request.POST["is_forever"]}')
        ban_form = BannedUserForm(request.POST)
        if ban_form.is_valid():
            if request.POST["is_forever"] == 'true':
                is_forever = True
            else:
                is_forever = False
            BannedUser.objects.create(offender=current_user,
                                      reason=request.POST["reason"],
                                      is_forever=is_forever)
            return HttpResponseRedirect(reverse("articles:author_profile", args=[pk]))
        else:
            messages.error(request, 'ошибка')
    else:
        ban_form = BannedUserForm()
    page_data = {
        'title': title,
        'ban_form': ban_form,
        'current_user_pk': pk,
    }
    return render(request, 'moderator/add_ban.html', page_data)


def banned_users(request):
    title = "Заблокированные пользователи"
    banned_users = BannedUser.objects.filter(is_active=True)
    page_data = {
        'title': title,
    }
    return render(request, "moderator/banned_users.html", page_data)


