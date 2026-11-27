from django.conf import settings
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


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    score = models.IntegerField(default=0)
    games_played = models.PositiveIntegerField('Games played', default=0)
    wins = models.PositiveIntegerField('Wins', default=0)
    current_streak = models.PositiveIntegerField('Current streak', default=0)

    class Meta:
        ordering = ['-score', 'user_id']


    @property 
    def losses(self):
        return max(0,self.games_played - self.wins)

    @property
    def win_rate(self):
        if not self.games_played:
            return 0 
        return round (min(self.wins, self.games_played) * 100 / self.games_played)

    def record_result(self, won):
        self.games_played += 1
        if won:
            self.wins += 1 
            self.current_streak += 1
        else:
            self.current_streak  = 0 
        self.save(update_fields=['games_played', 'wins', 'current_streak'])

    def __str__(self):
        return f'{self.user.username}: {self.score}'
