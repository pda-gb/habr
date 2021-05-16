import datetime

from django.core.mail import send_mail
from django.db import models, transaction
from django.utils.timezone import now

from apps.articles.models import Article
from apps.authorization.models import HabrUser
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
    reason = models.TextField(verbose_name='причина блокировки')

    class Meta:
        verbose_name = "нарушитель"
        verbose_name_plural = "нарушители"
        ordering = ('-date_ban',)

    def get_remaining_days(self):
        remaining_days = None
        if not self.is_forever:
            num_days = self.num_days
            date_ban = self.date_ban
            end_date = date_ban + datetime.timedelta(days=num_days)
            current_date = datetime.date.today()
            remaining_days = (end_date - current_date).days
            if remaining_days <= 0:
                self.is_active = False
                self.save()
                self.unset_ban_email()
        return remaining_days

    def delete(self):
        self.is_active = False
        self.save()

    def set_ban_email(self):
        """
        Функция отправляет письмо с оповещением о блокировке аккаунта.
        """
        user = HabrUser.objects.get(username=self.offender)
        subject = f'Блокировка пользователя {user.username}'
        message = f'Здравствуйте!\nВаш аккаунт был заблокирован' \
                  f' {"навсегда" if self.is_forever else f"на {self.num_days} дней"}\n' \
                  f'по причине: {self.reason}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def unset_ban_email(self):
        """
        Функция отправляет письмо с оповещением о снятии бана.
        """
        user = HabrUser.objects.get(username=self.offender)
        subject = f'Снятие блокировки пользователя {user.username}'
        message = 'Здравствуйте!\nСрок блокировки вашего аккаунта истёк, доступ к нему вновь разрешён.'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


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
    remark = models.TextField(blank=False,
                              verbose_name="Замечание модератора")
    fixed = models.BooleanField(default=False,
                                help_text="автор исправил статью")

    @staticmethod
    @transaction.atomic
    def send_article_to_verify(pk_article, pk_author):
        """отправка статьи на проверку"""
        article = Article.objects.filter(pk=pk_article, author_id=pk_author,
                                         draft=True)
        if article.exists():
            if VerifyArticle.objects.filter(
                    verification=pk_article).exists():

                send_article = VerifyArticle.objects.filter(
                    verification=Article.objects.get(id=pk_article)
                )
                send_article.update(is_verified=None)
            else:
                send_article = VerifyArticle.objects.create(
                    verification=Article.objects.get(id=pk_article)
                )
                send_article.is_verified = None
                send_article.save()

            Article.objects.filter(id=pk_article).update(updated=now())
            return True
        else:
            return None

    @staticmethod
    def get_status_verification_article(pk_article):
        """
        запрос статуса проверки текущей статьи
        """
        status = False
        if VerifyArticle.objects.filter(verification=pk_article).exists():
            is_verified = VerifyArticle.objects.get(verification=pk_article
                                                       ).is_verified
            if is_verified is None:
                status = True

        return status

    # @staticmethod
    # def get_status_verification_articles(pk_author):
    #     """
    #     запрос статуса проверки всех статей и причин отказов
    #     в публикации автора
    #     """
    #     status = []
    #     if VerifyArticle.objects.filter(
    #             verification__author_id=pk_author).exists():
    #         for itm in VerifyArticle.objects.filter(
    #                 verification__author_id=pk_author):
    #             status.append(
    #                 (itm.verification_id, itm.is_verified, itm.remark)
    #             )
    #     else:
    #         status = None
    #     return status


    @staticmethod
    def get_articles_with_statuses(pk_author, draft=None):
        """
        Формирование объекта из статьи и текущего статуса модерации
        """
        articles_with_statuses = []
        articles = Article.get_by_author(pk_author, draft)
        for article in articles:
            if VerifyArticle.objects.filter(verification=article.pk).exists():
                articles_with_statuses.append(
                    (
                        article,
                        VerifyArticle.objects.get(
                            verification=article.pk).is_verified,
                        VerifyArticle.objects.get(
                            verification=article.pk).remark)

                )
            else:
                # если статья не отправлялась на проверку и отредактирована
                articles_with_statuses.append((article, 'not_checked'))
        return articles_with_statuses


    @staticmethod
    def get_all_articles_for_verifications():
        """получение всех статей на проверку"""
        verif_articles = VerifyArticle.objects.filter(
            is_verified=None).order_by('verification__created')
        articles_to_review = []
        for itm in verif_articles:
            articles_to_review.append(itm.verification)
        return articles_to_review


    @staticmethod
    def allow_publishing(id_article):
        """Разрешение модератором публикации статьи"""
        VerifyArticle.objects.filter(
            verification=id_article).update(is_verified=True)
        Article.objects.filter(id=id_article).update(draft=False)
        Article.objects.filter(id=id_article).update(published=now(),
                                                     updated=now())


    @staticmethod
    def return_article(text_remark, id_article):
        """отправка на доработку и с обязательной причиной отказа"""
        VerifyArticle.objects.filter(verification=id_article).update(
            is_verified=False,
            remark=text_remark
        )
        Article.objects.filter(id=id_article)


    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
