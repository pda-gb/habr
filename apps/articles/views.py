from django.shortcuts import render

from apps.articles.models import Article, Hub


def main_page(request):
    """рендер главной страницы"""
    title = "главная страница"
    hub_articles = Article.get_articles()
    last_articles = hub_articles.values('id','title')[0:3]
    hubs_menu = Hub.get_all_hubs()
    page_data = {"title": title, "articles": hub_articles,
                 "hubs_menu": hubs_menu, "last_articles": last_articles}
    return render(request, "articles/articles.html", page_data)


def hub(request, pk=None):
    if pk == 1:
        hub_articles = Article.get_articles()
    else:
        hub_articles = Article.get_by_hub(pk)
    hubs_menu = Hub.get_all_hubs()
    page_data = {"articles": hub_articles, "hubs_menu": hubs_menu}
    return render(request, "articles/articles.html", page_data)


def article(request, pk=None):
    current_article = Article.get_article(pk)
    hubs_menu = Hub.get_all_hubs()
    page_data = {"article": current_article, "hubs_menu": hubs_menu}
    return render(request, "articles/article.html", page_data)
