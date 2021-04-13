from django.shortcuts import render
from apps.articles.models import Article

def user_articles(request):
    """
    функция отвечает за Мои статьи
    """
    title = 'Мои статьи'
    articles = Article.get_by_author(author_pk=request.user.id)
    page_data = {
        'title': title,
        'articles': articles,
    }
    return render(request, 'user_articles/user_articles.html', page_data)


def publications(request):
    """
    функция отвечает за мои публикации
    """
    title = 'Мои публикации'
    articles = Article.get_by_author(author_pk=request.user.id, draft=0)
    page_data = {
        'title': title,
        'articles': articles,
    }
    return render(request, 'user_articles/publications.html', page_data)


def draft(request):
    """
    функция отвечает за Черновик
    """
    title = 'Черновик'
    articles = Article.get_by_author(author_pk=request.user.id, draft=1)
    page_data = {
        'title': title,
        'articles': articles,
    }
    return render(request, 'user_articles/draft.html', page_data)
