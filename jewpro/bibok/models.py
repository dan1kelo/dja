from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveBigIntegerField('years')
    genre = models.CharField(max_length=100)
    poster = models.CharField(max_length=100)



    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return f'{self.title} ({self.year})'

    @property
    def poster_url(self):
        return f'https://image.tmdb.org/t/p/w500/{self.poster}'
