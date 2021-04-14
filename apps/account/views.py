from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from apps.account.forms import HabrUserProfileEditForm, ArticleCreate
from apps.articles.models import Article, Hub


@login_required
def add_article(request):
    if request.method == "POST":
        article_add = ArticleCreate(request.POST)
        if article_add.is_valid():
            article_add.save(commit=False)
            article_add.instance.author = request.user
            article_add.save()
            return HttpResponseRedirect(reverse("user_articles:user_articles"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    title = "Создание статьи"
    hubs_menu = Hub.get_all_hubs()
    article_add = ArticleCreate()
    page_data = {
        "title": title,
        "hubs_menu": hubs_menu,
        "article_add": article_add
    }
    return render(request, "account/form_add_article.html", page_data)


def del_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.del_article(pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def draft_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.draft_article(pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@transaction.atomic()
def edit_profile(request):
    title = "Редактирование профиля"
    if request.method == "POST":
        profile_edit_form = HabrUserProfileEditForm(
            request.POST, instance=request.user
        )
        if profile_edit_form.is_valid():
            profile_edit_form.save()
            return HttpResponseRedirect(reverse("account:edit_profile"))
    hubs_menu = Hub.get_all_hubs()
    profile_edit_form = HabrUserProfileEditForm(instance=request.user)
    page_data = {
        "title": title,
        "hubs_menu": hubs_menu,
        "edit_form": profile_edit_form,
    }
    return render(request, "account/edit_profile.html", page_data)
