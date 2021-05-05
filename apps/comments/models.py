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
        related_name="comment_parent",
        on_delete=models.CASCADE,
    )
    body = RichTextUploadingField()
    date = models.DateTimeField(verbose_name="дата", auto_now_add=True)
    is_child = models.BooleanField(default=False)
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

    def get_offset(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return level

    def get_col(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return level

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
