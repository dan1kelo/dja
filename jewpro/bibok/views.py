from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Movie, Profile


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        Profile.objects.create(user=user)
        login(request, user)
        return redirect('game')
    return render(request, 'registration/register.html', {'form': form, 'title': 'Регистрация'})


def _profile(request):
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        return profile
    return None



def home(request):
    return render(request, 'main.html', {'title': 'Jewpro'})


def _new_round(request):
    movie = Movie.objects.order_by('?').first()
    request.session['movie_id'] = movie.id if movie else None
    request.session['tries'] = 0
    request.session['history'] = []
    request.session['status'] = None


def game(request):
    if 'movie_id' not in request.session:
        _new_round(request)

    movie = Movie.objects.filter(id=request.session['movie_id']).first()
    if movie is None:
        _new_round(request)
        movie = Movie.objects.filter(id=request.session['movie_id']).first()

    profile = _profile(request)
    tries = request.session['tries']
    status = request.session['status']
    hint = ''
    if tries >= 4:
        hint = f'Год — {movie.year}, жанр — {movie.genre}' if movie else ''
    elif tries >= 2:
        hint = f'Год — {movie.year}' if movie else ''

    return render(request, 'game.html', {
        'title': 'gusse the movie ',
        'movie': movie,
        'movies': Movie.objects.order_by('title'),
        'tries': tries,
        'status': status,
        'hint': hint,
        'blur': max(0, 20 - tries * 4),
        'lives': ['x'] * tries + ['o'] * (5 - tries),
        'history': request.session['history'],
        'score': profile.wins if profile else request.session.get('score', 0),
    })


@require_POST
def guess(request):
    if request.session.get('status') is None and request.session.get('movie_id'):
        movie = Movie.objects.get(id=request.session['movie_id'])
        answer = request.POST.get('title', '').strip()
        if answer:
            request.session['tries'] += 1
            profile = _profile(request)
            if answer.casefold() == movie.title.casefold():
                request.session['status'] = 'win'
                request.session['score'] = request.session.get('score', 0) + 1
                if profile:
                    profile.wins += 1
                    profile.games += 1
                    profile.save()
            else:
                request.session['history'] = request.session['history'] + [answer]
                if request.session['tries'] >= 5:
                    request.session['status'] = 'lose'
                    if profile:
                        profile.games += 1
                        profile.save()
    return redirect('game')


@require_POST
def next_movie(request):
    _new_round(request)
    return redirect('game')
