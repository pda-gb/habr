from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from apps.articles.models import Article, ArticleRate
from apps.authorization.models import HabrUser, HabrUserProfile
from apps.comments.forms import CommentCreateForm
from apps.comments.models import Comment


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
    comments = Comment.get_comments(pk)
    # for comment in comments:
    #     print(f'{comment.child_comments.values() =}')
    form_comment = CommentCreateForm(request.POST or None)
    comments_is_liked = None
    comments_is_disliked = None
    if request.user.is_authenticated:
        rate = ArticleRate.create(current_article, request.user)
        current_article.user_liked = rate.liked
        current_article.bookmarked = rate.in_bookmarks
        comments_is_liked = Comment.get_liked_comments_by_user(pk,
                                                               request.user.id)
        comments_is_disliked = Comment.get_disliked_comments_by_user(
            pk,
            request.user.id
        )
    page_data = {
        "article": current_article,
        "last_articles": last_articles,
        "comments": comments,
        "form_comment": form_comment,
        "media_url": settings.MEDIA_URL,
        "comments_is_liked": comments_is_liked,
        "comments_is_disliked": comments_is_disliked,
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
        article_rate.article.dislikes = article_objects.filter(
            liked=False).count()
        article_rate.article.bookmarks = article_objects.filter(
            in_bookmarks=True
        ).count()
        article_rate.article.rating = (
                article_rate.article.likes - article_rate.article.dislikes
        )
        article_rate.article.save()
        article_rate.save(True)
        return JsonResponse(
            {
                "likes": article_rate.article.likes,
                "dislikes": article_rate.article.dislikes,
                "author_rating": article_rate.article.author.habruserprofile.rating,
                "liked": article_rate.liked,
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


def like_dislike_author_ajax(request):
    if request.is_ajax() and request.user.is_authenticated:
        user = request.GET.get("user")
        field = request.GET.get("field")
        if request.user.pk != int(user):
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
        return JsonResponse(
            {
                "karma": user.karma,
                "liked": user.karma_positive.filter(
                    pk=request.user.pk
                ).exists(),
                "disliked": user.karma_negative.filter(
                    pk=request.user.pk
                ).exists(),
            }
        )
