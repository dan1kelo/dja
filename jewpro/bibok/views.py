from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Movie


def home(request):
    return render(request, 'main.html', {'title': 'Jewpro'})


def _new_round(request):
    player = request.session.get('player', [])

    qs = Movie.objects.exclude(id__in=player)
    if not qs.exists():
        player = []
        qs = Movie.objects.all()

    movie = qs.order_by('?').first()
    if movie:
        player = player + [movie.id]
    request.session['movie_id'] = movie.id if movie else None
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
        return ''.join(''.join(out).split(' '))



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


    return render(request, 'game.html', {
        'title': 'Guess the movie',
        'movie': movie,
        'movies': Movie.objects.order_by('title'),
        'tries': tries,
        'status': status,
        'hint': hint,
        'blur': 0 if status else max(0, 20 - tries * 4),
        'lives': ['x'] * tries + ['o'] * (5 - tries),
        'history': request.session['history'],
        'score': request.session.get('score', 0),
    })


@require_POST
def guess(request):
    if request.session.get('status') is None and request.session.get('movie_id'):
        movie = Movie.objects.get(id=request.session['movie_id'])
        answer = request.POST.get('title', '').strip()
        if answer:
            request.session['tries'] += 1
            if answer.casefold() == movie.title.casefold():
                request.session['status'] = 'win'
                request.session['score'] = request.session.get('score', 0) + max(
                    1, WIN_POINTS - HINT_COST * request.session.get('hints', 0))
            else:
                request.session['history'] = request.session['history'] + [answer]
                if request.session['tries'] >= 5:
                    request.session['status'] = 'lose'
    return redirect('game')


@require_POST
def next_movie(request):
    _new_round(request)
    return redirect('game')



@require_POST
def hint(request):
    if request.session.get('status') is None and request.session.get('movie_id'):
        hints = request.session.get('hints', 0)
        score = request.session.get('score', 0)
        if hints < 3 and score >= HINT_COST:
            request.session['hints'] = hints + 1 
            request.session['score'] = score - HINT_COST
        return redirect('game')

@require_POST
def give_up(request):
    if request.session.get('status') is None and request.session.get('movie_id'):
        request.session['status'] = 'lose'
    return redirect('game')