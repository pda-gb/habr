from django.shortcuts import render


def login(request):
    title = 'Авторизация'
    page_data = {
        'title': title,
    }
    return render(request, 'authorization/login.html', page_data)


def register(request):
    title = 'Регистрация'
    page_data = {
        'title': title,
    }
    return render(request, 'authorization/register.html', page_data)
