from django.conf import settings
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveBigIntegerField('years')
    genre = models.CharField(max_length=100)
    poster = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return f'{self.title} ({self.year})'

    @property
    def poster_url(self):
        return f'https://image.tmdb.org/t/p/w500/{self.poster}'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wins = models.PositiveBigIntegerField(default=0)
    games = models.PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user.username}: {self.wins}/{self.games}'
