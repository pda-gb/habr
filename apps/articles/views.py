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
from django.shortcuts import render
from django.http import JsonResponse
from apps.articles.models import Article, ArticleRate


def main_page(request):
    """рендер главной страницы"""
    title = "главная страница"
    hub_articles = Article.get_articles()
    last_articles = Article.get_last_articles(hub_articles)
    page_data = {
        "title": title,
        "articles": hub_articles,
        "last_articles": last_articles,
    }
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
    # last_articles = Article.get_last_articles(current_article)
    current_article = get_object_or_404(Article, id=pk)
    hubs_menu = Hub.get_all_hubs()
    current_comments = Comment.get_comments(pk)
    comments = create_comments_tree(current_comments)
    form_comment = CommentCreateForm(request.POST or None)
    page_data = {

        "article": current_article,
        # "last_articles": last_articles
        "comments": comments,
        "form_comment": form_comment,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "articles/article.html", page_data)


def change_article_rate(request):
    if request.is_ajax():
        user = request.GET.get("user")
        article = request.GET.get("article")
        field = request.GET.get("field")
        article_rate = ArticleRate.objects.get(user=user, article=article)
        if field == "like":
            article_rate.liked = (
                True
                if article_rate.liked is None or article_rate.liked is False
                else None
            )
        elif field == "dislike":
            article_rate.liked = (
                False
                if article_rate.liked is None or article_rate.liked is True
                else None
            )
        else:
            article_rate.in_bookmarks = not article_rate.in_bookmarks
        article_rate.save()
        article_objects = ArticleRate.objects.filter(article=article)
        article_rate.article.likes = article_objects.filter(liked=True).count()
        article_rate.article.dislikes = article_objects.filter(liked=False).count()
        article_rate.article.bookmarks = article_objects.filter(in_bookmarks=True).count()
        article_rate.article.rating = article_rate.article.likes - article_rate.article.dislikes
        article_rate.article.save()
        article_rate.save(True)
        return JsonResponse(
            {
                "likes": article_rate.article.likes,
                "dislikes": article_rate.article.dislikes,
                "author_rating": article_rate.article.author.habruserprofile.rating,
                "liked": article_rate.liked
            }
        )
