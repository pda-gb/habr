from apps.articles.models import Hub


def get_verify_flag(request):
    """
    Получить флаг подтверждения регистрации
    """
    check_verify = request.session.get('verify', None)
    # print('*'*100)
    # print(check_verify)
    # request.session.clear_expired()
    return {
        "check_verify": check_verify,
    }
