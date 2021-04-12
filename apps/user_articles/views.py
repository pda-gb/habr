from django.shortcuts import render


def user_articles(request):
    """
    функция отвечает за Мои статьи
    """
    title = 'Мои статьи'

    page_data = {
        'title': title,
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
