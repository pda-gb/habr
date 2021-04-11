from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from apps.authorization.forms import HabrUserLoginForm, HabrUserRegisterForm, HabrUserEditRegisterForm


def login(request):
    """
    функция выполняет авторизацию
    """
    title = 'Авторизация'
    login_form = HabrUserLoginForm(data=request.POST or None)
    if request.method == "POST" and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main_page'))

    page_data = {
        'title': title,
        'login_form':login_form
    }
    return render(request, 'authorization/login.html', page_data)

def logout(request):
    """
    функция выполняет выход из аккаунта
    """
    auth.logout(request)
    return HttpResponseRedirect(reverse('main_page'))

def register(request):
    """
    функция выполняет регистрацию
    """
    title = 'Регистрация'

    if request.method == 'POST':
        register_form = HabrUserRegisterForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse("auth:login"))
    register_form = HabrUserRegisterForm()

    page_data = {
        'title': title,
        'register_form': register_form
    }
    return render(request, 'authorization/register.html', page_data)

def edit(request):
    """
    функция выполняет Изменение данных для входа
    """
    title = 'Изменение данных для входа'

    if request.method == 'POST':
        edit_form = HabrUserEditRegisterForm(request.POST, instance=request.user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("auth:login"))
    edit_form = HabrUserRegisterForm(instance=request.user)

    page_data = {
        'title': title,
        'edit_form': edit_form
    }
    return render(request, 'authorization/edit.html', page_data)

def forgive(request):
    """
    Функция отвечающая если забыли пароль
    """

    title = 'Забыл пароль'
    page_data = {
        'title':title,
    }
    return render(request, 'authorization/forgive.html', page_data)
