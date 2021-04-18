
from django.db import models
from django.utils import timezone
import datetime
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

from apps.articles.models import Article
from apps.authorization.models import HabrUser, HabrUserProfile

# Create your models here.
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    path = ArrayField(models.IntegerField(),default=[])
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(verbose_name='Текст статьи')

    created = models.DateTimeField(verbose_name="создан", default=timezone.now)
    updated = models.DateTimeField(verbose_name="обновлен", auto_now=True)
    
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
        comments = Comment.objects.filter(article__pk=article_pk).order_by('updated')
        return comments
