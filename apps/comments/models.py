from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models

from apps.articles.models import Article
from apps.authorization.models import HabrUser


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="child_comments",
        on_delete=models.CASCADE,
    )
    body = RichTextUploadingField()
    date = models.DateTimeField(verbose_name="дата", auto_now_add=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="лайки",
        related_name="comment_likes",
        through="LikesCommentViewed",
        blank=True,
    )
    dislikes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="дизлайки",
        related_name="comment_dislikes",
        through="DislikesCommentViewed",
        blank=True,
    )
    viewed = models.BooleanField(default=False, verbose_name='просмотрено')

    def __str__(self):
        return f"{self.article.title}-{self.author.username}"

    @property
    def get_parent(self):
        if not self.parent:
            return ""
        else:
            return self.parent

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"

    @staticmethod
    def create_comment(article_pk, comment_pk, author_pk, text_comment):
        try:
            comment_object = Comment.objects.get(pk=comment_pk)
        except ValueError:
            comment_object = None
        author = HabrUser.objects.get(pk=author_pk)
        article = Article.objects.get(pk=article_pk)
        comment = Comment(
            body=text_comment, article=article, author=author, comment_to=comment_object
        )
        comment.save()

    @staticmethod
    def get_comments(article_pk):
        comments = Comment.objects.filter(article__pk=article_pk).order_by("date")
        return comments

    @staticmethod
    def get_all_comments():
        comments = Comment.objects.all()
        return comments

    @staticmethod
    def get_all_comments_hub(pk):
        articles = Article.get_articles().filter(hub=pk, draft=False)
        return articles

    @staticmethod
    def get_comment(parent_id):
        ''' получение родительского комментария '''
        comment = Comment.objects.get(id=parent_id)
        return comment

    @staticmethod
    def get_all_users_liked_comment(id_comment):
        """Выдаёт id всех юзеров, которые лайкнули данный комментарий"""
        id_users = LikesCommentViewed.objects.all().filter(
            comment=id_comment)
        return id_users

    @staticmethod
    def get_all_users_disliked_comment(id_comment):
        """Выдаёт id всех юзеров, которые дизлайкнули данный комментарий"""
        id_users = DislikesCommentViewed.objects.all().filter(
            comment=id_comment)
        return id_users

    @staticmethod
    def check_liked_comment_by_user(id_comment, id_user):
        """проверяет лайкнул ли юзер комментарий"""
        # all_users = Comment.get_all_liked_comment_users(id_comment)
        if LikesCommentViewed.objects.filter(comment=id_comment,
                                             user=id_user).exists():
            return True
        return False

    @staticmethod
    def check_disliked_comment_by_user(id_comment, id_user):
        """проверяет дизлайкнул ли юзер комментарий"""
        # all_users = Comment.get_all_liked_comment_users(id_comment)
        if DislikesCommentViewed.objects.filter(comment=id_comment,
                                                user=id_user).exists():
            return True
        return False

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
