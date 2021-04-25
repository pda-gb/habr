from apps.comments.forms import CommentCreateForm
from apps.comments.models import Comment
from apps.comments.utils import create_comments_tree
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from apps.articles.models import Article
from apps.authorization.models import HabrUser


def main_page(request):
    """рендер главной страницы"""
    title = "главная страница"
    hub_articles = Article.get_articles()
    last_articles = Article.get_last_articles(hub_articles)
    page_data = {
        "title": title,
        "articles": hub_articles,
        "last_articles": last_articles,
        "current_user": request.user,
    }
    return render(request, "articles/articles.html", page_data)


def hub(request, pk=None):
    hub_articles = Article.get_articles()
    last_articles = Article.get_last_articles(hub_articles)
    if pk != 1:
        hub_articles = Article.get_by_hub(pk)
    page_data = {"articles": hub_articles, "last_articles": last_articles}
    return render(request, "articles/articles.html", page_data)


def article(request, pk=None):
    hub_articles = Article.get_articles()
    last_articles = Article.get_last_articles(hub_articles)
    current_article: Article = get_object_or_404(Article, id=pk)
    current_comments = Comment.get_comments(pk)
    comments = create_comments_tree(
        current_comments, request.user if request.user.is_authenticated else None
    )
    form_comment = CommentCreateForm(request.POST or None)
    if request.user.is_authenticated:
        current_article.views.add(request.user)
        current_article.liked = current_article.likes.filter(
            pk=request.user.pk
        ).exists()
        current_article.disliked = current_article.dislikes.filter(
            pk=request.user.pk
        ).exists()
        current_article.bookmarked = current_article.bookmarks.filter(
            pk=request.user.pk
        ).exists()
    page_data = {
        "article": current_article,
        "last_articles": last_articles,
        "comments": comments,
        "form_comment": form_comment,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "articles/article.html", page_data)


def change_article_rate(request):
    if request.is_ajax():
        article = request.GET.get("article")
        field = request.GET.get("field")
        article = Article.objects.get(pk=article)
        if field == "like":
            if article.likes.filter(pk=request.user.pk).exists():
                article.likes.remove(request.user)
            else:
                article.likes.add(request.user)
                article.dislikes.remove(request.user)
        elif field == "dislike":
            if article.dislikes.filter(pk=request.user.pk).exists():
                article.dislikes.remove(request.user)
            else:
                article.dislikes.add(request.user)
                article.likes.remove(request.user)
        else:
            if article.bookmarks.filter(pk=request.user.pk).exists():
                article.bookmarks.remove(request.user)
            else:
                article.bookmarks.add(request.user)
        article.rating = article.likes.count() - article.dislikes.count()
        article.author.habruserprofile.rating = article.rating
        article.author.save()
        article.save()
        return JsonResponse(
            {
                "likes": article.likes.count(),
                "dislikes": article.dislikes.count(),
                "author_rating": article.author.habruserprofile.rating,
                "like": article.likes.filter(pk=request.user.pk).exists(),
                "dislike": article.dislikes.filter(pk=request.user.pk).exists(),
            }
        )


def show_author_profile(request, pk=None):
    title = "Информация об авторе"
    author = get_object_or_404(HabrUser, pk=pk)
    page_data = {
        "title": title,
        "current_user": author,
    }
    return render(request, "articles/author_profile.html", page_data)
