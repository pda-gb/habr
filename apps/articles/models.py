from django.db import models
from django.utils import timezone

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
    author = models.ForeignKey(HabrUser, on_delete=models.CASCADE)
    hubs = models.ManyToManyField(Hub, verbose_name="хабы")
    tags = models.ManyToManyField(Tag, blank=True)
    body = models.TextField(verbose_name="Текст статьи")
    image = models.ImageField(blank=True, verbose_name="главная картинка")
    link_to_original = models.URLField(blank=True, verbose_name="ссылка на оригинал")

    created = models.DateTimeField(verbose_name="создана", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="обновлена", auto_now=True)
    published = models.DateTimeField(
        verbose_name="дата публикации", default=timezone.now
    )

    draft = models.BooleanField(verbose_name="черновик", default=False)
    is_active = models.BooleanField(verbose_name="удалена", default=True)

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        ordering = ("-published",)

    def __str__(self):
        return self.title

    @staticmethod
    def get_articles():
        """
        Returns all published articles
        """
        return Article.objects.filter(draft=False)

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
        articles = Article.get_articles()
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
        return Article.get_articles().filter(tags=tag)

    @staticmethod
    def get_by_hub(hub_id: int):
        """
        Returns articles with the set hub
        """
        return Article.get_articles().filter(hubs=hub_id)

    @staticmethod
    def get_by_author(author_pk: int):
        """
        Returns articles with the set author
        """
        return Article.get_articles().filter(author=author_pk)

    @staticmethod
    def del_article(id):
        """
        delete(is_active = False) article
        """
        art = Article.objects.get(id=id)
        art.is_active = False
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


if __name__ == "__main__":
    hub = Hub(hub="development")
