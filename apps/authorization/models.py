from django.contrib.auth.models import AbstractUser
from django.db import models


class HabrUser(AbstractUser):
    pass


class HabrUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='аватарка')
    user = models.OneToOneField(HabrUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name='настоящее имя', max_length=64, blank=True)
    place_of_work = models.CharField(verbose_name='место работы', max_length=256, blank=True)
    specialization = models.TextField(verbose_name='специализация', max_length=64, blank=True,
                                      default='пользователь')
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(verbose_name='страна', max_length=64, blank=True)
    region = models.CharField(verbose_name='регион', max_length=64, blank=True)
    city = models.CharField(verbose_name='город', max_length=64, blank=True)
