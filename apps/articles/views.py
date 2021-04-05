from django.shortcuts import render
from  apps.articles.models import Article


def main_page(request):
    """рендер главной страницы"""
    title = 'Главная страница'
    page_data = {
        'title': title,
        'articles': Article.get_annotation(),

    }
    return render(request, 'articles/index.html', page_data)