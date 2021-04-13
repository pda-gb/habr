from django.shortcuts import render
from apps.articles.models import Article

def user_articles(request):
    """
    функция отвечает за Мои статьи
    """
    title = 'Мои статьи'
    path = request.resolver_match.url_name
    if path == 'user_articles':
        articles = Article.get_by_author(author_pk=request.user.id)
    elif path == 'publications':
        articles = Article.get_by_author(author_pk=request.user.id, draft=0)
    elif path == 'draft':
        articles = Article.get_by_author(author_pk=request.user.id, draft=1)
    page_data = {
        'title': title,
        'articles': articles,
    }
    return render(request, 'user_articles/user_articles.html', page_data)

