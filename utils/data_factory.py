from mimesis import Person

from apps.authorization.models import HabrUser


def get_user(number):
    """
    Creates random user data
    :param number: number of users
    """
    for i in range(number):
        person = Person('ru')
        user = HabrUser(username=person.username(template='UU_d'),
                        email=person.email(domains=('yandex.ru', 'gmail.com')), password=person.password())
        user.save()


if __name__ == '__main__':
    get_user(10)
