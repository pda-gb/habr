from django.shortcuts import render
from django.http import JsonResponse
from apps.articles.models import Article, ArticleRate
from apps.authorization.models import HabrUserProfile


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
    author_rate = HabrUserProfile.objects.get(id=current_article.author.id).rating
    if request.user.is_authenticated:
        ArticleRate.create(current_article, request.user)
    page_data = {"article": current_article, "last_articles": last_articles,
                 "author_rate": author_rate}
    return render(request, "articles/article.html", page_data)


def change_article_rate(request):
    if request.is_ajax():
        user = request.GET.get("user")
        article = request.GET.get("article")
        field = request.GET.get("field")
        article_rate = ArticleRate.objects.get(user=user, article=article)
        author = HabrUserProfile.objects.get(id=Article.get_article(article).author.id)
        if field == "like":
            if article_rate.liked:
                article_rate.liked = None
                author.rating -= 1
            elif article_rate.liked == None:
                article_rate.liked = True
                author.rating += 1
            else:
                article_rate.liked = True
                author.rating += 2
        elif field == "dislike":
            if article_rate.liked == False:
                article_rate.liked = None
                author.rating += 1
            elif article_rate.liked == None:
                article_rate.liked = False
                author.rating -= 1
            else:
                article_rate.liked = False
                author.rating -= 2
        else:
            article_rate.in_bookmarks = not article_rate.in_bookmarks
        author.save()
        author_rating = author.rating
        article_rate.save()
        article_objects = ArticleRate.objects.filter(article=article)
        likes = article_objects.filter(liked=True).count()
        dislikes = article_objects.filter(liked=False).count()
        bookmarks = article_objects.filter(in_bookmarks=True).count()
        article_rate.article.likes = likes
        article_rate.article.dislikes = dislikes
        article_rate.article.bookmarks = bookmarks
        article_rate.article.save()
        return JsonResponse(
            {
                "likes": likes,
                "dislikes": dislikes,
                "bookmarks": bookmarks,
                "author_rating": author_rating,
            }
        )
