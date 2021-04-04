from django.db import models

from django.conf import settings
from django.utils import timezone

from apps.authorization.models import HabrUser


class Hub(models.Model):
    class Meta:
        verbose_name = 'хаб'
        verbose_name_plural = 'хабы'


class Tag(models.Model):
    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Article(models.Model):
    title = models.CharField(max_length=120, verbose_name='заголовок')
    author = models.ForeignKey(HabrUser, on_delete=models.CASCADE)
    hubs = models.ForeignKey(Hub)
    tags = models.ForeignKey(Tag, blank=True)
    body = models.TextField()

    created = models.DateTimeField(verbose_name='создана', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлена', auto_now=True)
    publish = models.DateTimeField(verbose_name='опубликована', default=timezone.now)

    is_delete = models.BooleanField(verbose_name='удалена', default=False)
    no_published = models.BooleanField(verbose_name='черновик', default=True)

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    @staticmethod
    def get_articles():
        return Article.objects.filter(no_published=False)

    def get_annotation(self):
        pass


