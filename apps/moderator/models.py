from django.db import models
import datetime
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
    date_ban = models.DateField(auto_now_add=True, verbose_name='дата блокировки')
    is_forever = models.BooleanField(default=False, verbose_name='Блокировка навсегда')
    num_days = models.IntegerField(verbose_name='дней блокировки', blank=True, default=0)
    is_active = models.BooleanField(default=False)
    reason = models.TextField(blank=True, verbose_name='причина блокировки')

    class Meta:
        verbose_name = "нарушитель"
        verbose_name_plural = "нарушители"
        ordering = ('-date_ban',)

    def get_remaining_days(self):
        num_days = self.num_days
        date_ban = self.date_ban
        end_date = date_ban + datetime.timedelta(days=num_days)
        current_date = datetime.date.today()
        remaining_days = (end_date - current_date).days
        if remaining_days < 0:
            self.is_active = False
            self.save()
        return remaining_days

    def delete(self):
        self.is_active = False
        self.save()


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
    for_checking = models.BooleanField(default=False,
                                       help_text="автор запросил проверку "
                                                 "иправления")

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"

# class Remark(models.Model):
#     """Замечания модератора и корректировки статьи автора"""
#     message = models.TextField(verbose_name="Замечание модератора")
#     correction = models.TextField(verbose_name="исправление")
