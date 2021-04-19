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


from .models import Article, Hub
from apps.comments.models import Comment

from apps.comments.models import Comment
from apps.comments.forms import CommentCreateForm


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
    if request.method == 'POST':
        form_comment = CommentCreateForm(request.POST or None)
        if form_comment.is_valid():
            form_comment = form_comment.save(commit=False)
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            form_comment.reply = comment_qs
            form_comment.author = request.user
            form_comment.article = current_article
            form_comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form_comment = CommentCreateForm()
    page_data = {
        "article": current_article,
        "hubs_menu": hubs_menu, 
        "last_articles": last_articles,
        "comments":current_comments,
        "form_comment":form_comment,
        "media_url": settings.MEDIA_URL,
    }
    #if request.is_ajax():
        #html = render_to_string('articles/article.html', context=page_data)
        #return JsonResponse({'form':html})
        
    return render(request, "articles/article.html", page_data)
