from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db import transaction
from apps.articles.models import Article, Hub
from apps.account.forms import HabrUserEditForm, HabrUserProfileEditForm


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
        edit_form = HabrUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_edit_form = HabrUserProfileEditForm(request.POST, instance=request.user.habruserprofile)
        if edit_form.is_valid() and profile_edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('account:edit_profile'))
    else:
        edit_form = HabrUserEditForm(instance=request.user)
        profile_edit_form = HabrUserProfileEditForm(instance=request.user.habruserprofile)

    avatar = request.user.avatar

    hubs_menu = Hub.get_all_hubs()
    page_data = {
        'title': title,
        'hubs_menu': hubs_menu,
        'edit_form': edit_form,
        'profile_edit_form': profile_edit_form,
        'avatar': avatar
    }
    return render(request, 'account/edit_profile.html', page_data)
