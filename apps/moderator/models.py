from django.db import models
from django.shortcuts import get_object_or_404

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
    date_ban = models.DateField(auto_now_add=True,
                                verbose_name='дата блокировки')
    is_forever = models.BooleanField(default=False,
                                     verbose_name='Блокировка навсегда')
    num_days = models.IntegerField(verbose_name='дней блокировки',
                                   blank=True, default=0)
    is_active = models.BooleanField(default=False)
    reason = models.TextField(blank=True, verbose_name='причина блокировки')

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


class BannedArticle(models.Model):
    """Забаненная статья"""
    delete = models.ForeignKey(Article, help_text="удалённая статья",
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = "удалённая статья"
        verbose_name_plural = "удалённые статьи"


class VerifyArticle(models.Model):
    """Проверка статьи модератором"""
    verification = models.ForeignKey(Article, help_text="статья на модерацию",
                                     on_delete=models.DO_NOTHING)
    is_verified = models.BooleanField(default=False,
                                      help_text="одобрение статьи")
    remark = models.TextField(blank=True, verbose_name="Замечание модератора")
    fixed = models.BooleanField(default=False,
                                help_text="автор исправил статью")

    # for_checking = models.BooleanField(default=False,
    #                                    help_text="автор запросил проверку "
    #                                              "иправления")

    @staticmethod
    def send_article_to_verify(pk_article, pk_author):
        """отправка статьи на проверку"""
        article = Article.objects.filter(pk=pk_article, author_id=pk_author,
                                         draft=True)
        if article.exists():
            VerifyArticle.objects.create(verification=Article.objects.get(id=pk_article))
            return True
        else:
            return None

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"

# class Remark(models.Model):
#     """Замечания модератора и корректировки статьи автора"""
#     message = models.TextField(verbose_name="Замечание модератора")
#     correction = models.TextField(verbose_name="исправление")
