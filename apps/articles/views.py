from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from apps.articles.models import Article
from apps.authorization.models import HabrUser, HabrUserProfile
from apps.comments.forms import CommentCreateForm
from apps.comments.models import Comment
from apps.comments.utils import create_comments_tree


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
    current_article = get_object_or_404(Article, id=pk)
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
        current_article.author_liked = (
            current_article.author.habruserprofile.karma_positive.filter(
                pk=request.user.pk
            ).exists()
        )
        current_article.author_disliked = (
            current_article.author.habruserprofile.karma_negative.filter(
                pk=request.user.pk
            ).exists()
        )
    page_data = {
        "article": current_article,
        "last_articles": last_articles,
        "comments": comments,
        "form_comment": form_comment,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "articles/article.html", page_data)


def change_article_rate(request):
    if request.is_ajax() and request.user.is_authenticated:
        article = request.GET.get("article")
        field = request.GET.get("field")
        article = Article.objects.get(pk=article)
        if request.user != article.author:
            if field == "like":
                if article.likes.filter(pk=request.user.pk).exists():
                    article.likes.remove(request.user)
                    article.author.habruserprofile.rating -= 1
                elif article.dislikes.filter(pk=request.user.pk).exists():
                    article.likes.add(request.user)
                    article.dislikes.remove(request.user)
                    article.author.habruserprofile.rating += 2
                else:
                    article.likes.add(request.user)
                    article.author.habruserprofile.rating += 1
            elif field == "dislike":
                if article.dislikes.filter(pk=request.user.pk).exists():
                    article.dislikes.remove(request.user)
                    article.author.habruserprofile.rating += 1
                elif article.likes.filter(pk=request.user.pk).exists():
                    article.dislikes.add(request.user)
                    article.likes.remove(request.user)
                    article.author.habruserprofile.rating -= 2
                else:
                    article.dislikes.add(request.user)
                    article.author.habruserprofile.rating -= 1
            else:
                if article.bookmarks.filter(pk=request.user.pk).exists():
                    article.bookmarks.remove(request.user)
                else:
                    article.bookmarks.add(request.user)
            article.rating = article.likes.count() - article.dislikes.count()
            article.author.habruserprofile.save()
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


def like_dislike_author_ajax(request):
    if request.is_ajax() and request.user.is_authenticated:
        user = request.GET.get("user")
        field = request.GET.get("field")
        if request.user.pk != user:
            user = HabrUserProfile.objects.get(pk=user)
            if field == "like":
                if user.karma_positive.filter(pk=request.user.pk).exists():
                    user.karma_positive.remove(request.user)
                elif user.karma_negative.filter(pk=request.user.pk).exists():
                    user.karma_positive.add(request.user)
                    user.karma_negative.remove(request.user)
                else:
                    user.karma_positive.add(request.user)
            elif field == "dislike":
                if user.karma_negative.filter(pk=request.user.pk).exists():
                    user.karma_negative.remove(request.user)
                elif user.karma_positive.filter(pk=request.user.pk).exists():
                    user.karma_negative.add(request.user)
                    user.karma_positive.remove(request.user)
                else:
                    user.karma_negative.add(request.user)
        user.save()
        return JsonResponse({})


def show_author_profile(request, pk=None):
    title = "Информация об авторе"
    author = get_object_or_404(HabrUser, pk=pk)
    page_data = {
        "title": title,
        "current_user": author,
    }
    return render(request, "articles/author_profile.html", page_data)
