from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

from apps.account.forms import ChangePasswordForm, ArticleEditForm
from apps.account.forms import HabrUserProfileEditForm, ArticleCreate
from apps.articles.models import Article, Hub
from apps.authorization.models import HabrUser


@login_required
@transaction.atomic()
def add_article(request):
    if request.method == "POST":
        article_add = ArticleCreate(request.POST, request.FILES)
        if article_add.is_valid():
            article_add.save(commit=False)
            article_add.instance.author = request.user
            article_add.save()
            return HttpResponseRedirect(reverse("account:user_articles"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    title = "Создание статьи"
    article_add = ArticleCreate()
    page_data = {"title": title, "article_add": article_add}
    return render(request, "account/form_add_article.html", page_data)


@login_required
@transaction.atomic()
def del_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.del_article(pk)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
@transaction.atomic()
def draft_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.draft_article(pk)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
@transaction.atomic()
def edit_profile(request):
    title = "Редактирование профиля"
    if request.method == "POST":
        profile_edit_form = HabrUserProfileEditForm(
            request.POST, request.FILES, instance=request.user.habruserprofile
        )
        if profile_edit_form.is_valid():
            profile_edit_form.save()
            return HttpResponseRedirect(reverse("account:edit_profile"))
    hubs_menu = Hub.get_all_hubs()
    profile_edit_form = HabrUserProfileEditForm(instance=request.user.habruserprofile)
    page_data = {
        "title": title,
        "hubs_menu": hubs_menu,
        "edit_form": profile_edit_form,
    }
    return render(request, "account/edit_profile.html", page_data)


@login_required
def user_articles(request):
    """
    функция отвечает за Мои статьи
    """
    title = "Мои статьи"
    articles = Article.get_by_author(author_pk=request.user.id)
    page_data = {
        "title": title,
        "articles": articles,
    }
    return render(request, "account/user_articles.html", page_data)


@login_required
def publications(request):
    """
    функция отвечает за мои публикации
    """
    title = "Мои публикации"
    articles = Article.get_by_author(author_pk=request.user.id, draft=0)
    page_data = {
        "title": title,
        "articles": articles,
    }
    return render(request, "account/user_articles.html", page_data)


@login_required
def draft(request):
    """
    функция отвечает за Черновик
    """
    title = "Черновик"
    articles = Article.get_by_author(author_pk=request.user.id, draft=1)
    page_data = {
        "title": title,
        "articles": articles,
    }
    return render(request, "account/user_articles.html", page_data)


@login_required
@transaction.atomic()
def edit_password(request):
    title = "Изменить пароль"
    user = HabrUser.objects.get(username=request.user)

    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")

            if check_password(old_password, user.password):
                user.password = make_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                return HttpResponseRedirect(reverse("account:user_articles"))
            else:
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    form = ChangePasswordForm()

    page_data = {
        "title": title,
        "edit_form": form,
    }
    return render(request, "account/edit_password.html", page_data)


@login_required
@transaction.atomic()
def edit_article(request, pk):
    """
    функция отвечает за редактирование статьи
    """
    title = "Создание статьи"
    edit_article = get_object_or_404(Article, pk=pk)

    if request.method == "POST":
        edit_form = ArticleEditForm(request.POST, request.FILES, instance=edit_article)
        if edit_form.is_valid():
            edit_article.updated = timezone.now()
            edit_article.save()
            edit_form.save()
            return HttpResponseRedirect(reverse("account:user_articles"))
    else:
        edit_form = ArticleEditForm(instance=edit_article)

    page_data = {
        "title": title,
        "update_form": edit_form,
        "media_url": settings.MEDIA_URL,
    }

    return render(request, "account/edit_article.html", page_data)
