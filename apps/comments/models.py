from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
import abc

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

    @staticmethod
    def get_all_comments():
        comments = Comment.objects.all()
        return comments

    @staticmethod
    def get_all_comments_hub(pk):
        articles = Article.get_articles().filter(hub=pk, draft=False)


class Sorted(abc.ABC):
    ''' класс отвечает за сортировку  '''

    @abc.abstractclassmethod
    def get_data(self, pk=None):
        pass

    @staticmethod
    def sort(sort_type, pk=None):
        TYPE = {
            '-date': SortDate,
            'like': SortLike,
            'view': SortView,
            'comments': SortComments,
        }
        if pk:
            return TYPE[sort_type](pk)
        else:
            return TYPE[sort_type]()

class SortDate(Sorted):

    def __init__(self, pk=None):
        self.pk = pk

    def get_data(self):
        if self.pk:
            return Article.objects.filter(hub=self.pk, draft=False).order_by('-updated')
        else:
            return Article.objects.filter(draft=False).order_by('-updated')

class SortLike(Sorted):

    def __init__(self, pk=None):
        self.pk = pk

    def get_data(self):
        if self.pk:
            return Article.objects.filter(hub=self.pk, draft=False).order_by('-rating')
        else:
            return Article.objects.filter(draft=False).order_by('-rating')

class SortView(Sorted):

    def __init__(self, pk=None):
            self.pk = pk

    def get_data(self):
        if self.pk:
            articles = Article.objects.filter(hub=self.pk, draft=False)
        else:
            articles = Article.objects.filter(draft=False)
        result = sorted(articles, key=lambda x: x.views.count(), reverse=True)
        return result

class SortComments(Sorted):

    def __init__(self, pk=None):
        self.pk = pk

    def get_data(self):
        comments = {}
        if self.pk:
            pass
        else:
            articles = Article.objects.filter(draft=False)
            for article in articles:
                current_comments = Comment.get_comments(article.id)
                comments[article] = current_comments.count()
        comments = sorted(comments.items(), key=lambda x:x[1] ,reverse=True)
        result = [i[0] for i in comments]
        return result