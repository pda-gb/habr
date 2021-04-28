from django.contrib import auth, messages
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from apps.authorization.forms import (
    HabrUserLoginForm,
    HabrUserRegisterForm,
)
from apps.authorization.models import HabrUser


def verify(request, email, activation_key):
    """
    Функция проверяет и активирует учётную запись пользователя
    """
    try:
        user = HabrUser.objects.get(activation_key=activation_key)
        if not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print('активация прошла успешно')
        else:
            messages.error(request, 'Ошибка активации')
        page_data = {
            'title': 'верификация',
        }
        return render(request, "authorization/verification.html", page_data)
    except Exception as e:
        messages.error(request, f'ошибка активации {e.args}')
        return HttpResponseRedirect(reverse('main_page'))


def send_verify_email(user):
    """
    Функция отправляет письмо с подтверждением регистрации пользователю
    """
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    subject = f'Активация пользователя {user.username}'
    message = f'Для подтверждения активации перейдите по ссылке:\n {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)



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
    from_register = request.session.get('register', None)
    if from_register:
        del request.session['register']
    page_data = {
        "title": title,
        "login_form": login_form,
        "from_register": from_register
    }
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
            user = register_form.save()
            if send_verify_email(user):
                request.session['register'] = True
            else:
                messages.error(request, 'Ошибка отправки сообщения')
            return HttpResponseRedirect(reverse("auth:login"))
        else:
            messages.error(request, "ЛОГИН ИЛИ ПАРОЛЬ ВВЕДЕНЫ НЕКОРРЕКТНО!")
    register_form = HabrUserRegisterForm()

    page_data = {
        "title": title,
        "register_form": register_form
    }
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


def change_username(request):
    """
    Функция изменяет логин пользователя
    """
    title = "Изменить логин"
    page_data = {
        'title': title,
    }

    return render(request, "authorization/change_username.html", page_data)

