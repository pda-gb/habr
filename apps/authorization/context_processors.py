from apps.articles.models import Hub


def get_verify_flag(request):
    """
    Получить флаг подтверждения регистрации
    """
    check_verify = request.session.get('verify', None)
    return {
        "check_verify": check_verify,
    }
