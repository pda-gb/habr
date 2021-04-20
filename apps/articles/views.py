from django.shortcuts import render
from django.http import JsonResponse
from apps.articles.models import Article, ArticleRate


def main_page(request):
    """рендер главной страницы"""
    title = "главная страница"
    hub_articles, last_articles = Article.get_articles()
    page_data = {
        "title": title,
        "articles": hub_articles,
        "last_articles": last_articles,
    }
    return render(request, "articles/articles.html", page_data)


def hub(request, pk=None):
    hub_articles, last_articles = Article.get_articles()
    if pk != 1:
        hub_articles = Article.get_by_hub(pk)
    page_data = {"articles": hub_articles, "last_articles": last_articles}
    return render(request, "articles/articles.html", page_data)


def article(request, pk=None):
    last_articles = Article.get_articles()[1]
    current_article = Article.get_article(pk)
    if request.user.is_authenticated:
        rate = ArticleRate.create(current_article, request.user)
        current_article.user_liked = rate.liked
        current_article.bookmarked = rate.in_bookmarks
    page_data = {"article": current_article, "last_articles": last_articles}
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
