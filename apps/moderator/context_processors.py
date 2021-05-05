from apps.moderator.models import Moderator


def check_is_staff(request):
    """
    Проверить является ли пользователь модератором.
    """
    is_staff = Moderator.objects.filter(staff=request.user.pk).exists()
    return {
        'is_staff': is_staff,
    }