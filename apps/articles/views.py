from django.shortcuts import render

from apps.articles.models import Article, Hub
from apps.authorization.models import HabrUser
from django.shortcuts import render, get_object_or_404

def main_page(request):
    """рендер главной страницы"""
    title = "главная страница"
    hub_articles, last_articles = Article.get_articles()
    page_data = {
        "title": title,
        "articles": hub_articles,
        "last_articles": last_articles,
        "current_user": request.user
    }
    return render(request, "articles/articles.html", page_data)


def hub(request, pk=None):
    hub_articles, last_articles = Article.get_articles()
    if pk != 1:
        hub_articles = Article.get_by_hub(pk)
    page_data = {
        "articles": hub_articles,
        "last_articles": last_articles
    }
    return render(request, "articles/articles.html", page_data)


def article(request, pk=None):
    last_articles = Article.get_articles()[1]
    current_article = Article.get_article(pk)
    page_data = {
        "article": current_article,
        "last_articles": last_articles
    }
    return render(request, "articles/article.html", page_data)


def show_author_profile(request, pk=None):
    title = "Информация об авторе"
    author = get_object_or_404(HabrUser, pk=pk)
    page_data = {
        "title": title,
        "current_user": author,
    }
    return render(request, "articles/author_profile.html", page_data)
