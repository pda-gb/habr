from django.conf import settings
from django.db import models

from apps.articles.models import Article
from apps.authorization.models import HabrUser, HabrUserProfile


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", null=True, related_name="child_comments", on_delete=models.CASCADE
    )
    body = models.TextField(verbose_name="текст комментария")
    date = models.DateTimeField(verbose_name="дата", auto_now_add=True)

    # is_child = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.article.title}-{self.author.username}"

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"

    @staticmethod
    def create_comment(article_pk: int, comment_pk: int, username, text_comment):
        try:
            parent_comment = Comment.objects.get(pk=comment_pk)
        except ValueError:
            parent_comment = None
        print(f'{username=}')
        author = username
        print(f'{author=}')
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
