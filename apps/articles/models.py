from django.db import models
from django.db.models.fields import BooleanField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
import datetime
from django.conf import settings

from apps.authorization.models import HabrUser


class Hub(models.Model):
    hub = models.CharField(max_length=100)

    class Meta:
        verbose_name = "хаб"
        verbose_name_plural = "хабы"

    @staticmethod
    def get_all_hubs():
        """
        Returns all hubs as dict
        """
        hubs_menu = []
        hubs = Hub.objects.all()
        for itm in hubs:
            itm_menu = {"id": itm.id, "hub": itm.hub}
            hubs_menu.append(itm_menu)
        return hubs_menu

    # для отображения названий вместо id в админке
    def __str__(self):
        return f"{self.hub}"


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Article(models.Model):
    title = models.CharField(max_length=120, verbose_name="заголовок")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hubs = models.ManyToManyField(Hub, verbose_name="хабы")
    tags = models.ManyToManyField(Tag, blank=True)
    body = models.TextField(verbose_name="Текст статьи")
    image = models.ImageField(
        upload_to="img_articles/", blank=True, verbose_name="главная картинка"
    )
    link_to_original = models.URLField(blank=True, verbose_name="ссылка на оригинал")

    created = models.DateTimeField(verbose_name="создана", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="обновлена", auto_now=True)
    published = models.DateTimeField(
        verbose_name="дата публикации", default=timezone.now
    )

    draft = models.BooleanField(verbose_name="черновик", default=False)
    is_active = models.BooleanField(verbose_name="удалена", default=True)

    likes = models.PositiveIntegerField(verbose_name="лайки", default=0)
    dislikes = models.PositiveIntegerField(verbose_name="дизлайки", default=0)
    views = models.PositiveIntegerField(verbose_name="просмотры", default=0)
    bookmarks = models.PositiveIntegerField(verbose_name="заметки", default=0)
    rating = models.IntegerField(verbose_name="рейтинг", default=0)

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        ordering = ("-published",)

    def __str__(self):
        return self.title

    @staticmethod
    def get_articles():
        """
        Returns all published articles and last articles (right block)
        """
        hub_articles = Article.objects.filter(draft=False)
        len_last_articles = 3
        last_articles_set = hub_articles.values("id", "title", "published")[
            0:len_last_articles
        ]
        last_articles = [{} for _ in range(len_last_articles)]
        for i in range(len_last_articles):
            last_articles[i]["id"] = last_articles_set[i]["id"]
            last_articles[i]["title"] = last_articles_set[i]["title"]
            if (
                last_articles_set[i]["published"].date()
                != datetime.datetime.now().date()
            ):
                last_articles[i]["date"] = last_articles_set[i]["published"].date()
            else:
                last_articles[i]["date"] = "сегодня"
            last_articles[i]["time"] = last_articles_set[i]["published"].strftime(
                "%H:%M"
            )
        return hub_articles, last_articles

    @staticmethod
    def get_article(id_article):
        """
        Returns article
        """
        return Article.objects.get(id=id_article)

    @staticmethod
    def get_annotation(word_count: int) -> tuple:
        """
        Return a dictionary, where the key is pk, and the value is the
        first 'word_count' words of the article.
        """
        annotation = []
        articles = Article.get_articles()[0]
        for article in articles:
            body_list = article.body.split(" ")[:word_count]
            itm_annotation = {
                "body": " ".join(body_list),
                "title": article.title,
                "id": article.id,
                "published": article.published,
                "username": article.author,
            }
            annotation.append(itm_annotation)

        # собипраем хабы для отображения кликабельного меню хабов
        hubs_menu = Hub.get_all_hubs()
        return annotation, hubs_menu

    @staticmethod
    def get_by_tag(tag: str):
        """
        Returns articles with the set tag
        """
        return Article.get_articles()[0].filter(tags=tag)

    @staticmethod
    def get_by_hub(hub_id: int):
        """
        Returns articles with the set hub
        """
        return Article.get_articles()[0].filter(hubs=hub_id)

    @staticmethod
    def get_by_author(author_pk: int, draft=None):
        """
        Returns articles with the set author
        """
        if draft is None:
            return Article.objects.filter(author_id__pk=author_pk).order_by("updated")
        return (
            Article.objects.filter(author_id__pk=author_pk)
            .filter(draft=draft)
            .order_by("-updated")
        )

    @staticmethod
    def del_article(id):
        """
        delete(is_active = False) article
        """
        art = Article.objects.get(id=id)
        art.is_active = False
        art.save()

    @staticmethod
    def draft_article(id):
        """
        turn draft article(True/False)
        """
        art = Article.objects.get(id=id)
        if art.draft is False:
            art.draft = True
        else:
            art.draft = False
        art.save()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment_to = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE
    )
    author = models.ForeignKey(HabrUser, on_delete=models.CASCADE)
    body = models.TextField()

    created = models.DateTimeField(verbose_name="создан", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="обновлен", auto_now=True)
    publish = models.DateTimeField(verbose_name="опубликован", default=timezone.now)

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


class ArticleRate(models.Model):
    article = ForeignKey(Article, on_delete=models.CASCADE)
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked = BooleanField(null=True, default=None)
    watched = BooleanField(default=True)
    in_bookmarks = BooleanField(default=False)

    def save(self, rating=None, force_insert=None, using=None) -> None:
        super().save(force_insert=force_insert, using=using)
        if rating:
            rating = Article.objects.filter(author=self.article.author).values_list("rating")
            self.article.author.habruserprofile.rating = sum(rate[0] for rate in rating)
            self.article.author.habruserprofile.save()

    @staticmethod
    def create(article, user):
        try:
            return ArticleRate.objects.get(article=article, user=user)
        except Exception:
            article.views += 1
            article.save()
            return ArticleRate.objects.create(article=article, user=user)


if __name__ == "__main__":
    hub = Hub(hub="development")
