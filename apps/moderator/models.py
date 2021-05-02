from django.db import models

from apps.articles.models import Article
from apps.comments.models import Comment
from habr import settings


class Moderator(models.Model):
    """Модератор"""
    staff = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "модератор"
        verbose_name_plural = "модераторы"


class BannedUser(models.Model):
    """Забаненный пользователь"""
    offender = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "нарушитель"
        verbose_name_plural = "нарушители"


class BannedComment(models.Model):
    """Забаненный комментарий"""
    wrong = models.ForeignKey(Comment,
                              on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "удалённый комментарий"
        verbose_name_plural = "удалённые комментарии"


class VerifyArticle(models.Model):
    """Проверка статьи модератором"""
    verification = models.ForeignKey(Article,
                                     on_delete=models.DO_NOTHING)


    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
