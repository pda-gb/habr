from django.shortcuts import render

from apps.articles.models import Article, Hub


def main_page(request):
    """рендер главной страницы"""
    title = "главная страница"
    hub_articles = Article.get_articles()
    last_articles = Article.get_last_articles(hub_articles)
    page_data = {
        "title": title,
        "articles": hub_articles,
        "last_articles": last_articles}
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
    current_article = Article.get_article(pk)
    # last_articles = Article.get_last_articles(current_article)
    page_data = {
        "article": current_article,
        # "last_articles": last_articles
    }
    return render(request, "articles/article.html", page_data)
