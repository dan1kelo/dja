import random

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Movie, Profile

LEADERS_COUNT = 10


def _profile(user):
    return Profile.objects.get_or_create(user=user)[0]


def _add_score(user, delta):
    profile = _profile(user)
    profile.score = max(0, profile.score + delta)
    profile.save(update_fields=['score'])


def _record_result(user, won):
    _profile(user).record_result(won)


@login_required
def home(request):
    return render(request, 'main.html', {'title': 'Jewpro'})


def _new_round(request):
    player = request.session.get('player', [])
    all_ids = list(Movie.objects.values_list('id', flat=True))
    free = [i for i in all_ids if i not in player]
    if not free:
        free = [i for i in all_ids if i != (player[-1] if player else None)] or all_ids
        player = []

    movie_id = random.choice(free) if free else None 
    if movie_id:
        player = player + [movie_id]
    request.session['movie_id'] = movie_id
    request.session['player'] = player
    request.session['tries'] = 0
    request.session['history'] = []
    request.session['status'] = None
    request.session['hints'] = 0

WIN_POINTS = 10 
LIMIT_TRIES = 5 
HINT_COST = 2 


def _mask(title, opened):
    out, shown = [], 0
    for ch in title:
        if not ch.isalnum():
            out.append(ch)
        elif shown < opened:
            out.append(ch)
            shown += 1 
        else:
            out.append('_')
    return ''.join(out)



@login_required
def game(request):
    if 'movie_id' not in request.session:
        _new_round(request)

    movie = Movie.objects.filter(id=request.session['movie_id']).first()
    if movie is None:
        _new_round(request)
        movie = Movie.objects.filter(id=request.session['movie_id']).first()

    tries = request.session['tries']
    status = request.session['status']
    hint = ''
    if tries >= 4:
        hint = f'Age — {movie.year}, genre — {movie.genre}' if movie else ''
    elif tries >= 2:
        hint = f'Year — {movie.year}' if movie else ''

    hints = request.session.get('hints', 0 )
    if movie and hints and not status:
        hint = (hint + ' | ' if hint else '') + f'Title: {_mask(movie.title, hints)}'


    leaders = Profile.objects.select_related('user').order_by('-score', 'user_id')[:LEADERS_COUNT]
    return render(request, 'game.html', {
        'leaders': leaders,
        'title': 'Guess the movie',
        'movie': movie,
        'movies': Movie.objects.order_by('title'),
        'tries': tries,
        'status': status,
        'hint': hint,
        'blur': 0 if status else max(0, 20 - tries * 4),
        'lives': ['x'] * tries + ['o'] * (5 - tries),
        'history': request.session['history'],
        'score': _profile(request.user).score,
        'hint_cost': HINT_COST,
        'can_hint': hints < 3,
        'reward': max(1, WIN_POINTS - HINT_COST * hints),
    })


@login_required
@require_POST
def guess(request):
    if request.session.get('status') is None and request.session.get('movie_id'):
        movie = Movie.objects.get(id=request.session['movie_id'])
        answer = request.POST.get('title', '').strip()
        if answer:
            request.session['tries'] += 1
            if answer.casefold() == movie.title.casefold():
                request.session['status'] = 'win'
                _record_result(request.user, True)
                _add_score(request.user, max(
                    1, WIN_POINTS - HINT_COST * request.session.get('hints', 0)))
            else:
                request.session['history'] = request.session['history'] + [answer]
                if request.session['tries'] >= 5:
                    request.session['status'] = 'lose'
                    _record_result(request.user, False)
    return redirect('game')


@require_POST
def next(request):
    _new_round(request)
    return redirect('game')


@login_required
@require_POST
def hint(request):
    if request.session.get('status') is None and request.session.get('movie_id'):
        hints = request.session.get('hints', 0)
        if hints < 3 and _profile(request.user).score >= HINT_COST:
            request.session['hints'] = hints + 1
            _add_score(request.user, -HINT_COST)
    return redirect('game')

@login_required
@require_POST
def restart(request):
    if request.session.get('status') is None and request.session.get('movie_id'):
        request.session['status'] = 'lose'
        _record_result(request.user, False)
    return redirect('game')


@login_required
def profile(request):
    return render(request, 'profile.html', {
        'title': 'Profile',
        'profile': _profile(request.user),
    })


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'logo.html', {'title': 'Login', 'form': form})


def signup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.save())
        return redirect('home')
    return render(request, 'signUp.html', {'title': 'Sign up', 'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')
