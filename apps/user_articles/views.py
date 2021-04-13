from django.shortcuts import render
from apps.articles.models import Article, Hub

def user_articles(request):
    """
    функция отвечает за Мои статьи
    """
    title = 'Мои статьи'
    articles = Article.objects.filter(author_id__pk=request.user.id).order_by('updated')
    print(articles)
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

    page_data = {
        'title': title,
    }
    return render(request, 'user_articles/publications.html', page_data)


def draft(request):
    """
    функция отвечает за Черновик
    """
    title = 'Черновик'

    page_data = {
        'title': title,
    }
    return render(request, 'user_articles/draft.html', page_data)
