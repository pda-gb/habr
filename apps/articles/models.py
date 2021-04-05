from django.db import models

from django.conf import settings
from django.utils import timezone

from apps.authorization.models import HabrUser


class Hub(models.Model):
    hub = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'хаб'
        verbose_name_plural = 'хабы'


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Article(models.Model):
    title = models.CharField(max_length=120, verbose_name='заголовок')
    author = models.ForeignKey(HabrUser, on_delete=models.CASCADE)
    hubs = models.ManyToManyField(Hub)
    tags = models.ManyToManyField(Tag, blank=True)
    body = models.TextField()
    image = models.ImageField(blank=True, verbose_name='картинка')
    link_to_original = models.URLField(blank=True, verbose_name='ссылка на оригинал')

    created = models.DateTimeField(verbose_name='создана', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлена', auto_now=True)
    published = models.DateTimeField(verbose_name='дата публикации', default=timezone.now)

    draft = models.BooleanField(verbose_name='черновик', default=True)

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ('-published',)

    def __str__(self):
        return self.title

    @staticmethod
    def get_articles():
        """
        Returns all published articles
        """
        return Article.objects.filter(draft=False)

    def get_annotation(self):
        pass


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(HabrUser, on_delete=models.CASCADE)
    body = models.TextField()

    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    publish = models.DateTimeField(verbose_name='опубликован', default=timezone.now)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
