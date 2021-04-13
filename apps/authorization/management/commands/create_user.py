from django.contrib import auth
from django.utils import timezone
from mimesis import Person, Business, Datetime, Address

from apps.authorization.models import HabrUser, HabrUserProfile
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Created random article data. Format python manage.py create_article number_article' \
           'First create user'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help=u'Количество создаваемых статей')

    def handle(self, *args, **options):
        """
        Creates random the article data
        """
        person = Person('ru')
        business = Business('ru')
        datetime = Datetime('ru')
        address = Address('ru')
        number = options['number']
        for i in range(number):
            user = HabrUser(username=person.username(template='UU_d'),
                            email=person.email(domains=('yandex.ru', 'gmail.com')),
                            password=person.password(length=8, hashed=False))
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created user {user.username}'))

            profile = HabrUserProfile(user=user, avatar=person.avatar(size=256),
                                      full_name=person.full_name(gender=None, reverse=False),
                                      place_of_work=business.company(), specialization=person.occupation(),
                                      gender=person.gender(iso5218=False, symbol=False),
                                      birth_date=datetime.date(start=1950, end=2018),
                                      country=address.country(allow_random=False),
                                      region=address.region(),
                                      city=address.city())
            profile.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully created profile {profile.full_name}'))
