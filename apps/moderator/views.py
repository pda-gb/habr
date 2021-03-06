from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
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

    if request.method == 'POST':
        ban_form = BannedUserForm(request.POST)
        if ban_form.is_valid():
            # if request.POST["is_forever"] == 'true':
            #     is_forever = True
            # else:
            #     is_forever = False
            banned_user_query = BannedUser.objects.filter(offender=pk)
            if banned_user_query:
                banned_user = banned_user_query[0]
                banned_user.is_active = True
                banned_user.reason = request.POST["reason"]
                banned_user.num_days = request.POST["num_days"]
                banned_user.date_ban = datetime.today()
                banned_user.save()
            else:
                BannedUser.objects.create(offender=current_user,
                                          reason=request.POST["reason"],
                                          num_days=request.POST["num_days"],
                                          is_active=True)
                                          # is_forever=is_forever)
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


def remove_user_ban(request, pk):
    current_user = BannedUser.objects.get(offender=pk)
    current_user.is_active = False
    current_user.save()
    return HttpResponseRedirect(reverse("articles:author_profile", args=[pk]))


def banned_users(request):
    title = "Заблокированные пользователи"
    page_data = {
        'title': title,
    }
    return render(request, "moderator/banned_users.html", page_data)


