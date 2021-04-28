from random import randint, choice

from django.core.management.base import BaseCommand
from mimesis import Text, Internet

from apps.articles.models import Hub, Tag, Article
from apps.authorization.models import HabrUser
from apps.comments.models import Comment


class Command(BaseCommand):
    help = (
        "Created random article data. Format python manage.py "
        "create_article number_article"
    )


    def add_arguments(self, parser):
        parser.add_argument("number", type=int,
                            help="Количество создаваемых статей")

    def get_random_query_set_item(self, my_model):
        """
        Creates a randoms instance of the model
        """
        pks = my_model.objects.values_list("pk", flat=True).order_by("id")
        if pks:
            random_pk = choice(pks)
            return my_model.objects.get(pk=random_pk)
        else:
            print(f"Таблицы {my_model} нет в базе данных")
            pass

    @staticmethod
    def get_list_models(my_model):
        return list(
            my_model.objects.values_list("pk", flat=True)
                .order_by("?")
                .distinct()[: randint(1, 5)]
        )

    def handle(self, *args, **options):
        """
        Creates random data for an article
        """
        # Экземпляры данных из библиотеки mimesis
        text = Text("ru")
        hubs = [
            "Разработка",
            "Дизайн",
            "Маркетинг",
            "Мобильная разработка",
        ]
        internet = Internet("ru")
        # Количество создаваемых статей
        number = options["number"]
        # number = 100
        # Создаем хабы
        for hub_item in hubs:
            if hub_item in Hub.objects.values_list("hub",
                                                   flat=True).distinct():
                self.stdout.write(self.style.SUCCESS(f"This hub exist "
                                                     f"{hub_item}"))
            else:
                hub_object = Hub(hub=hub_item)
                hub_object.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created hub "
                                       f"{hub_object.hub}")
                )
        # Создаем теги в количестве, равном половине статей.
        for i in range(number // 2):
            tag_object = Tag(tag=internet.hashtags(quantity=1))
            if tag_object.tag in Tag.objects.values_list("tag",
                                                         flat=True).distinct():
                self.stdout.write(
                    self.style.SUCCESS(f"This tag exist {tag_object.tag}")
                )
            else:
                tag_object.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created tag "
                                       f"{tag_object.tag}")
                )

        ## Создаем статьи
        # ключевые слова для поиска картинок
        keyword_img = ['it', 'development', 'design', 'marketing',
                       'mobile']
        for i in range(number):
            id_hub = randint(1, 4)
            article = Article(
                title=text.title(),
                author=self.get_random_query_set_item(HabrUser),
                body=text.text(quantity=randint(10, 70)),
                image=internet.stock_image(
                    width=1920, height=1080,
                    keywords=[keyword_img[0], keyword_img[id_hub]],
                    writable=False
                ),
                link_to_original=internet.home_page(tld_type=None),
                draft=False,
                hub=Hub.objects.get(id=id_hub)
            )

            article.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created article by the author "
                    f"{article.author}"
                )
            )

            # # Добавляем к статье хабы, выбранные случайным образом в количестве от 1 до 5
            # article.hub.add(*self.get_list_models(Hub))
            # for hub in article.hub.all():
            #     self.stdout.write(
            #         self.style.SUCCESS(
            #             f"Successfully added hub {hub.hub} to article {article.title}"
            #         )
            #     )

            # Добавляем к статье теги, выбранные случайным образом в
            # количестве от 1 до 5
            article.tags.add(*self.get_list_models(Tag))
            for tag in article.tags.all():
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created tag {tag.tag}")
                )

            # Создаем комментарии к статье
            for _ in range(randint(0, 5)):
                comment = Comment(
                    author=self.get_random_query_set_item(HabrUser),
                    # comment_to=None,
                    article=article,
                    body=text.text(quantity=randint(1, 10)),
                )
                comment.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created comment to article "
                        f"{comment.article.author}"
                    )
                )

            # # Создаем комментарии к комментариям
            # if Comment.objects.all().count():
            #     for _ in range(randint(0, 5)):
            #         comment_to_comment = Comment(
            #             author=self.get_random_query_set_item(HabrUser),
            #             article=article,
            #             comment_to=self.get_random_query_set_item(Comment),
            #             body=text.text(quantity=randint(1, 10)),
            #         )
            #         comment_to_comment.save()
            #         self.stdout.write(
            #             self.style.SUCCESS(
            #                 f"Successfully created comment to comment "
            #                 f"{comment_to_comment.comment_to.author}"
            #             )
            #         )
