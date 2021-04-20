from django.contrib import auth, messages
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from apps.authorization.forms import (
    HabrUserLoginForm,
    HabrUserRegisterForm,
)


def login(request):
    """
    функция выполняет авторизацию
    """
    title = "Авторизация"
    login_form = HabrUserLoginForm(data=request.POST or None)
    if request.method == "POST" and login_form.is_valid():
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("articles:main_page"))
    page_data = {"title": title, "login_form": login_form}
    return render(request, "authorization/login.html", page_data)


def logout(request):
    """
    функция выполняет выход из аккаунта
    """
    auth.logout(request)
    return HttpResponseRedirect(reverse("articles:main_page"))


def register(request):
    """
    функция выполняет регистрацию
    """
    title = "Регистрация"

    if request.method == "POST":
        register_form = HabrUserRegisterForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse("auth:login"))
        else:
            messages.error(request, "ЛОГИН ИЛИ ПАРОЛЬ ВВЕДЕНЫ НЕКОРРЕКТНО!")
    register_form = HabrUserRegisterForm()

    page_data = {"title": title, "register_form": register_form}
    return render(request, "authorization/register.html", page_data)


def forgive(request):
    """
    Функция отвечающая если забыли пароль
    """

    title = "Забыл пароль"
    page_data = {
        "title": title,
    }
    return render(request, "authorization/forgive.html", page_data)
