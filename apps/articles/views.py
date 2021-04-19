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
    hub_articles, last_articles = Article.get_articles()
    hubs_menu = Hub.get_all_hubs()
    page_data = {"title": title, "articles": hub_articles,
                 "hubs_menu": hubs_menu, "last_articles": last_articles}
    return render(request, "articles/articles.html", page_data)


def hub(request, pk=None):
    hub_articles, last_articles = Article.get_articles()
    if pk != 1:
        hub_articles = Article.get_by_hub(pk)
    hubs_menu = Hub.get_all_hubs()
    page_data = {"articles": hub_articles, "hubs_menu": hubs_menu, "last_articles": last_articles}
    return render(request, "articles/articles.html", page_data)

def article(request, pk=None):
    last_articles = Article.get_articles()[1]
    current_article = get_object_or_404(Article, id=pk)
    hubs_menu = Hub.get_all_hubs()
    current_comments = Comment.get_comments(article_pk=pk)
    comments = create_comments_tree(current_comments)
    form_comment = CommentCreateForm(request.POST or None)
    page_data = {
        "article": current_article,
        "hubs_menu": hubs_menu, 
        "last_articles": last_articles,
        "comments":comments,
        "form_comment":form_comment,
        "media_url": settings.MEDIA_URL,
    }
        
    return render(request, "articles/article.html", page_data)

def create_comment(request, pk):
    current_article = get_object_or_404(Article, id=pk)
    form_comment = CommentCreateForm(request.POST or None)
    if form_comment.is_valid():
            new_comment = form_comment.save(commit=False)
            new_comment.author = request.user
            new_comment.article = current_article
            new_comment.body = form_comment.cleaned_data['body']    
            new_comment.parent = None
            new_comment.is_child = False
            new_comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@transaction.atomic
def create_child_comment(request, pk):
    user_name = request.user.username
    current_id = request.POST.get('id')
    current_article = get_object_or_404(Article, id=pk)
    text = request.POST.get('text')
    user = HabrUser.objects.get(username=user_name)
    parent = Comment.objects.get(id=int(current_id))
    is_child = False if not parent else True

    Comment.objects.create(
        article=current_article,
        author=user,
        body=text,
        parent=parent,
        is_child = is_child
    )
    
    comments_ = Comment.get_comments(pk)
    comments_list = create_comments_tree(comments_)
    page_data = {
        "media_url": settings.MEDIA_URL,
        'comments': comments_list,
    }
    return render(request, 'articles/article.html', context=page_data)