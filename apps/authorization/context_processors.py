from apps.articles.models import Hub


def get_verify_flag(request):
    """
    Получить флаг подтверждения регистрации
    """
    check_verify = request.session.get('verify', None)
    request.session.clear_expiried()
    return {
        "check_verify": check_verify,
    }
