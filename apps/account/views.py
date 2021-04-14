from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from apps.account.forms import HabrUserProfileEditForm, ArticleCreate, ChangePasswordForm
from apps.articles.models import Article, Hub
from apps.authorization.models import HabrUser

from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django import forms

def get_articles(request):
    # при создании модели User нужно будет добавить фильтровку по пользователю
    title = "Список статей"
    len_article_body = 5
    data = Article.get_annotation(len_article_body)
    hubs_menu = Hub.get_all_hubs()
    page_data = {"articles": data[0], "title": title, "hubs_menu": hubs_menu}
    return render(request, "account/account.html", page_data)


@login_required
def add_article(request):
    if request.method == "POST":
        article_add = ArticleCreate(request.POST)
        if article_add.is_valid():
            article_add.save(commit=False)
            article_add.instance.author = request.user
            article_add.save()
            return HttpResponseRedirect(reverse("account:articles_list"))

    title = "Создание статьи"
    hubs_menu = Hub.get_all_hubs()
    article_add = ArticleCreate()
    page_data = {
        "title": title,
        "hubs_menu": hubs_menu,
        "article_add": article_add
    }
    return render(request, "account/form_add_article.html", page_data)


@login_required
@transaction.atomic()
def edit_profile(request):
    title = "Редактирование профиля"
    if request.method == "POST":
        profile_edit_form = HabrUserProfileEditForm(
            request.POST, instance=request.user.habruserprofile
        )
        if profile_edit_form.is_valid():
            profile_edit_form.save()
            return HttpResponseRedirect(reverse("account:articles_list"))
        # return HttpResponseRedirect(reverse("account:edit_password"))
    hubs_menu = Hub.get_all_hubs()
    profile_edit_form = HabrUserProfileEditForm(instance=request.user.habruserprofile)
    page_data = {
        "title": title,
        "hubs_menu": hubs_menu,
        "edit_form": profile_edit_form,
    }
    return render(request, "account/edit_profile.html", page_data)


@login_required
# @transaction.atomic()
def edit_password(request):
    title = "Изменить пароль"
    user = HabrUser.objects.get(username=request.user)

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            repeat_password = request.POST.get("repeat_password")
            # old_password = make_password(old_password)
            # print(old_password)
            # print(user.password)
            # print(new_password)
            # if old_password == user.password:
            # print(check_password(old_password, user.password))
            # if user.check_password(old_passw):
            if check_password(old_password, user.password):
                print('*'*100)
                user.password = make_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                return HttpResponseRedirect(reverse("account:articles_list"))
            else:
                print('-'*100)
                forms.ValidationError('Ошибка!')
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                return HttpResponseRedirect(reverse("account:articles_list"))

    form = ChangePasswordForm()
    hubs_menu = Hub.get_all_hubs()

    page_data = {
        "title": title,
        "hubs_menu": hubs_menu,
        "edit_form": form,
    }
    return render(request, "account/edit_password.html", page_data)
