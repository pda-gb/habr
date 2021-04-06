# создание быстрых команд для выполнения частых задач ($: python manage.py make_fill_db )
# если из json файла в базу добавляется в поле с  UNIQUE=True уже имеющееся значение, то будет ошибка
import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from apps.articles.models import Article

path_json = os.path.join(settings.BASE_DIR, 'json')  # путь к json папке


def load_from_json(file_name):
    """
    :param file_name: имя необходимого json файла
    :return: выводит содержимое
    """
    with open(os.path.join(path_json, file_name + '.json'), 'r',
              encoding='utf-8') as file_json:
        return json.load(file_json)


class Command(BaseCommand):  # свой класс унаследуем от BaseCommand
    def handle(self, *args, **options):  # с обязательным методом handle

        # tags = load_from_json("tags")
        # count_tags = len(tags)
        # for itm in tags:
        # # распаковка словаря соответственно модели и распред. по ключам с
        # # одновременным сохр. в базу( .save() )
        # Tag.objects.create(**itm)
        #
        # hubs = load_from_json("hubs")
        # count_tags = len(hubs)
        # for itm in hubs:
        #     Tag.objects.create(**itm)

        articles = load_from_json("test_articles")
        for itm in articles:
            Article.objects.create(**itm)
