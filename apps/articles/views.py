from django.shortcuts import render

from apps.articles.models import Article


def main_page(request):
    """рендер главной страницы"""
    title = 'главная страница'
    len_article_body = 5
    articles = Article.get_annotation(len_article_body)
    page_data = {
        'title': title,
        'articles': articles,
    }
    return render(request, 'articles/articles.html', page_data)


def article(request, pk=None):
    # title = ''
    article = Article.get_article(pk)
    page_data = {
        # 'title': article.title,
        'article': article,
    }
    return render(request, 'articles/article.html', page_data)
