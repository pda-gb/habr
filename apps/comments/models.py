from django.conf import settings
from django.db import models

from apps.articles.models import Article
from apps.authorization.models import HabrUser, HabrUserProfile


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    parent = models.ForeignKey("self", null=True, blank=True,
                               related_name="comment_parent",
                               on_delete=models.CASCADE,
                               )
    body = models.TextField(verbose_name="текст комментария")
    date = models.DateTimeField(verbose_name="дата", auto_now_add=True)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="лайки",
        related_name="comment_likes",
        blank=True,
    )
    dislikes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="дизлайки",
        related_name="comment_dislikes",
        blank=True,
    )

    def __str__(self):
        return f"{self.article.title}-{self.author.username}"

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"

    @staticmethod
    def create_comment(article_pk: int, comment_pk: int, username,
                       text_comment):
        try:
            parent_comment = Comment.objects.get(pk=comment_pk)
        except ValueError:
            parent_comment = None
        author = username
        article = Article.objects.get(pk=article_pk)
        comment = Comment(
            body=text_comment, article=article, author=author,
            parent=parent_comment
        )
        comment.save()

    @staticmethod
    def get_comments(article_pk):
        comments = Comment.objects.filter(
            article__pk=article_pk).order_by("date")
        return comments

    @staticmethod
    def get_comment(parent_id):
        """ получение родительского комментария """
        comment = Comment.objects.get(id=parent_id)
        return comment

    @staticmethod
    def get_liked_comments_by_user(id_comment, id_user):
        """Проверка всех комментариев, на лайк от пользователя(для отметки
        в шаблоне, что текущий юзер уже лайкнул комментарий)"""
        liked_comments = []
        for itm in LikesCommentViewed.objects.filter(user=id_user):
            liked_comments.append(itm.comment.id)
        return liked_comments

    @staticmethod
    def get_disliked_comments_by_user(id_comment, id_user):
        """Проверка всех комментариев, на дизлайк от пользователя(для отметки
        в шаблоне, что текущий юзер уже дизлайкнул комментарий)"""
        disliked_comments = []
        for itm in DislikesCommentViewed.objects.filter(user=id_user):
            disliked_comments.append(itm.comment.id)
        return disliked_comments

class LikesCommentViewed(models.Model):
    """
    Расширение промежуточной таблицы дополнением
    поля просмотра уведомления
     """
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False, verbose_name='просмотрено')


class DislikesCommentViewed(models.Model):
    """
    Расширение промежуточной таблицы дополнением
    поля просмотра уведомления
     """
    comment = models.ForeignKey(Comment,
                                   on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False, verbose_name='просмотрено')