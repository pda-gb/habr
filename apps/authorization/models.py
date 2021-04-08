from django.db import models
from django.contrib.auth.models import AbstractUser


class HabrUser(AbstractUser):
    user_name = models.CharField(max_length=100, verbose_name='имя')
