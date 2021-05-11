import datetime

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

    @staticmethod
    def is_moderator(id_user: int) -> bool:
        """Проверка юзера явлляется ли он модератором"""
        return Moderator.objects.filter(staff=id_user).exists()


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
                                     on_delete=models.DO_NOTHING,
                                     related_name="verification_article")
    is_verified = models.BooleanField(null=True,
                                      verbose_name="статус проверки",
                                      help_text="None - статья в процессе "
                                                "проверки,True - одобрение "
                                                "статьи, False - отказ")
    remark = models.TextField(blank=True, verbose_name="Замечание модератора")
    fixed = models.BooleanField(default=False,
                                help_text="автор исправил статью")

    @staticmethod
    def send_article_to_verify(pk_article, pk_author):
        """отправка статьи на проверку"""
        article = Article.objects.filter(pk=pk_article, author_id=pk_author,
                                         draft=True)
        if article.exists():
            VerifyArticle.objects.create(
                verification=Article.objects.get(id=pk_article)
            )
            return True
        else:
            return None

    @staticmethod
    def get_status_verification_articles(pk_author):
        """запрос статуса проверки всех статей автора"""
        status = []
        if VerifyArticle.objects.filter(
                verification__author_id=pk_author).exists():
            for itm in VerifyArticle.objects.filter(
                    verification__author_id=pk_author):
                status.append(
                    (itm.verification_id, itm.is_verified)
                )
        else:
            status = None
        return status

    @staticmethod
    def get_all_articles_for_verifications():
        """получение всех статей на проверку"""
        verif_articles = VerifyArticle.objects.filter(
            is_verified=None).order_by('verification__created')
        articles_to_review = []
        for itm in verif_articles:
            articles_to_review.append(itm.verification)
        return articles_to_review

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
