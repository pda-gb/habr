from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views import View
from django.template.context_processors import csrf
from django.contrib import auth


from .models import Article, Hub
from apps.comments.models import Comment

from apps.comments.views import get_comments
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

@login_required
def article(request, pk=None):
    last_articles = Article.get_articles()[1]
    current_article = get_object_or_404(Article, id=pk)
    hubs_menu = Hub.get_all_hubs()
    current_comments = get_comments(pk=pk)
    if request.method == "POST":
        form_comment = CommentCreateForm(request.POST)
        if form_comment.is_valid():
            form_comment = form_comment.save(commit=False)
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
    return render(request, "articles/article.html", page_data)

class ArticleView(View):
    template_name = 'articles/article.html'
    form_comment = CommentCreateForm

    def get(self, request, *args, **kwargs):
        last_articles = Article.get_articles()[1]
        current_article = get_object_or_404(Article, id=self.kwargs['pk'])
        hubs_menu = Hub.get_all_hubs()
        context = {}
        context.update(csrf(request))
        user = auth.get_user(request)
        context['comments'] = current_article.comment_set.all().order_by('path')
        context['next'] = current_article.get_absolute_url()
        context['article'] = current_article
        context['hubs_menu'] = hubs_menu
        context['last_articles'] = last_articles
        for el in context['comments']:
            print(el)
        if user.is_authenticated:
            context['form'] = self.form_comment

        return render(request, template_name=self.template_name, context=context)

@login_required
@require_http_methods('POST')
def add_comment(request, pk):

    form = CommentCreateForm(request.POST)
    article = get_object_or_404(Article, id=pk)

    if form.is_valid():
        comment = Comment()
        comment.path = []
        comment.article = article
        comment.author = auth.get_user(request)
        comment.body = form.cleaned_data['comment_area']
        comment.save()
        try:
            comment.path.extend(Comment.objects.get(id=form.cleaned_data['parent_comment']).path)
            comment.path.append(comment)
        except ObjectDoesNotExist:
            comment.path.append(comment)

        comment.save()

    return redirect(article.get_absolute_url())
