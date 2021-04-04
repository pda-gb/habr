from django.db import models
from django.contrib.auth.models import AbstractUser


class HabrUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='аватарка')
    age = models.PositiveSmallIntegerField(verbose_name='возраст', default=18)
