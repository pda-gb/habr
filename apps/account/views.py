from django.shortcuts import render

from apps.articles.models import Article, Hub


def get_articles(request):
    # при создании модели User нужно будет добавить фильтровку по пользователю
    title = 'Список статей'
    len_article_body = 5
    data = Article.get_annotation(len_article_body)
    hubs_menu = Hub.get_all_hubs()
    page_data = {
        'articles': data[0],
        'title': title,
        'hubs_menu': hubs_menu
    }
    return render(request, 'account/account.html', page_data)


def add_article(request):
    title = 'Создание статьи'
    hubs_menu = Hub.get_all_hubs()
    page_data = {
        'title': title,
        'hubs_menu': hubs_menu,
    }
    return render(request, 'account/form_add_article.html', page_data)


def edit_profile(request):
    title = 'Редактирование профиля'
    hubs_menu = Hub.get_all_hubs()
    page_data = {
        'title': title,
        'hubs_menu': hubs_menu,
    }
    return render(request, 'account/form_edit_profile.html', page_data)
