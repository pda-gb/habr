from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from apps.account.forms import HabrUserProfileEditForm
from apps.articles.models import Article, Hub


def get_articles(request):
    # при создании модели User нужно будет добавить фильтровку по пользователю
    title = 'Список статей'
    len_article_body = 5
    data = Article.get_annotation(len_article_body)
    hubs_menu = Hub.get_all_hubs()
    page_data = {
        'articles': data[0],
        'title': title,
        'hubs_menu': hubs_menu
    }
    return render(request, 'account/account.html', page_data)


def add_article(request):
    title = 'Создание статьи'
    hubs_menu = Hub.get_all_hubs()
    page_data = {
        'title': title,
        'hubs_menu': hubs_menu,
    }
    return render(request, 'account/form_add_article.html', page_data)


@login_required
@transaction.atomic()
def edit_profile(request):
    title = 'Редактирование профиля'

    if request.method == 'POST':
        profile_edit_form = HabrUserProfileEditForm(request.POST, instance=request.user.habruserprofile)
        if profile_edit_form.is_valid():
            profile_edit_form.save()
            return HttpResponseRedirect(reverse('account:edit_profile'))
    else:
        return HttpResponseRedirect(reverse('account:edit_profile'))

    hubs_menu = Hub.get_all_hubs()
    page_data = {
        'title': title,
        'hubs_menu': hubs_menu,
        'profile_edit_form': profile_edit_form
    }
    return render(request, 'account/edit_profile.html', page_data)
