from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Movie, Profile


class ProfileStatsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', password='pw12345!')
        self.profile = Profile.objects.create(user=self.user)
        movie = Movie.objects.create(title='Inception', year=2010, genre='Sci-Fi', poster='x.jpg')
        self.client.force_login(self.user)
        self.client.post(reverse('next'))
        session = self.client.session
        session['movie_id'] = movie.id
        session.save()

    def stats(self):
        self.profile.refresh_from_db()
        return self.profile.games_played, self.profile.wins, self.profile.current_streak

    def test_win(self):
        self.client.post(reverse('guess'), {'title': 'inception'})
        self.assertEqual(self.stats(), (1, 1, 1))

    def test_lose_counts_once(self):
        for _ in range(6):
            self.client.post(reverse('guess'), {'title': 'wrong'})
        self.assertEqual(self.stats(), (1, 0, 0))

    def test_give_up_counts_once(self):
        self.client.post(reverse('restart'))
        self.client.post(reverse('restart'))
        self.assertEqual(self.stats(), (1, 0, 0))

    def test_profile_page(self):
        Profile.objects.filter(pk=self.profile.pk).update(games_played=4, wins=3)
        self.assertContains(self.client.get(reverse('profile')), '75%')
