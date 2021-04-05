from django.shortcuts import render
from apps.articles.models import Article


def main_page(request):
    """рендер главной страницы"""
    title = 'главная страница'
    articles = Article.get_annotation()
    page_data = {
        'title': title,
        'articles': articles,

    }
    return render(request, 'articles/articles.html', page_data)