from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class HabrUser(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(max_length=150, unique=True, blank=True)
    is_confirmed = models.BooleanField(verbose_name='Подтвержден', default=False)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=24)))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True


class HabrUserProfile(models.Model):
    MALE = "M"
    FEMALE = "W"

    GENDER_CHOICES = (
        (MALE, "М"),
        (FEMALE, "Ж"),
    )

    avatar = models.ImageField(
        upload_to="avatars/", blank=True, verbose_name="аватарка"
    )
    user = models.OneToOneField(
        HabrUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE
    )
    first_name = models.CharField(
        verbose_name="настоящее имя", max_length=64, blank=True
    )
    last_name = models.CharField(
        verbose_name='фамилия', max_length=64, blank=True
    )
    place_of_work = models.CharField(
        verbose_name="место работы", max_length=256, blank=True
    )
    specialization = models.TextField(
        verbose_name="специализация", max_length=64, blank=True, default="пользователь"
    )
    gender = models.CharField(
        verbose_name="пол", max_length=1, choices=GENDER_CHOICES, blank=True
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name="дата рождения")
    country = models.CharField(verbose_name="страна", max_length=64, blank=True)
    region = models.CharField(verbose_name="регион", max_length=64, blank=True)
    city = models.CharField(verbose_name="город", max_length=64, blank=True)
    rating = models.FloatField(verbose_name="рейтинг", default=0)
    karma_positive = models.ManyToManyField(
        HabrUser,
        blank=True,
        verbose_name="положительная карма",
        related_name="karma_positive",
    )
    karma_negative = models.ManyToManyField(
        HabrUser,
        blank=True,
        verbose_name="отрицательная карма",
        related_name="karma_negative",
    )
    karma = models.IntegerField(verbose_name="карма", default=0)

    def __str__(self) -> str:
        return self.user.username

    def save(self, *args, **kwargs) -> None:
        if self.pk:
            self.karma = self.karma_positive.count() - self.karma_negative.count()
        return super().save(*args, **kwargs)

    @receiver(post_save, sender=HabrUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            HabrUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=HabrUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.habruserprofile.save()
