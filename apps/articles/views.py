from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views import View
from django.template.context_processors import csrf
from django.contrib import auth
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from apps.authorization.models import HabrUser

from .models import Article, Hub
from apps.comments.models import Comment

from apps.comments.models import Comment
from apps.comments.forms import CommentCreateForm

from apps.comments.utils import create_comments_tree


def main_page(request):
    """рендер главной страницы"""
    title = "главная страница"
    hub_articles = Article.get_articles()
    last_articles = Article.get_last_articles(hub_articles)
    page_data = {
        "title": title,
        "articles": hub_articles,
        "last_articles": last_articles}
    return render(request, "articles/articles.html", page_data)


def hub(request, pk=None):
    hub_articles = Article.get_articles()
    last_articles = Article.get_last_articles(hub_articles)
    if pk != 1:
        hub_articles = Article.get_by_hub(pk)
    page_data = {
        "articles": hub_articles,
        "last_articles": last_articles
    }
    return render(request, "articles/articles.html", page_data)


def article(request, pk=None):
    # TODO какие последние 3 статьи должны выводиться в ЛК ?
    current_article = Article.get_article(pk)
    # last_articles = Article.get_last_articles(current_article)
    page_data = {
        "article": current_article,
        # "last_articles": last_articles
        "comments": comments,
        "form_comment": form_comment,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "articles/article.html", page_data)
