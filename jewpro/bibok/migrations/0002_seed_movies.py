from django.db import migrations

MOVIES = [
    ('Крёстный отец', 1972, 'Криминал, драма', '3bhkrj58Vtu7enYsRolD1fZdja1.jpg'),
    ('Бойцовский клуб', 1999, 'Драма, триллер', 'pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg'),
    ('Криминальное чтиво', 1994, 'Криминал', 'd5iIlFn5s0ImszYzBPb8JPIfbXD.jpg'),
    ('Побег из Шоушенка', 1994, 'Драма', '9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg'),
    ('Тёмный рыцарь', 2008, 'Боевик, криминал', 'qJ2tW6WMUDux911r6m7haRef0WH.jpg'),
    ('Начало', 2010, 'Фантастика', 'ljsZTbVsrQSqZgWeep2B1QiDKuh.jpg'),
    ('Интерстеллар', 2014, 'Фантастика, драма', 'gEU2QniE6E77NI6lCU6MxlNBvIx.jpg'),
    ('Форрест Гамп', 1994, 'Драма, комедия', 'arw2vcBveWOVZr6pxd9XTd1TdQa.jpg'),
    ('Матрица', 1999, 'Фантастика, боевик', 'f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg'),
]


def add_movies(apps, schema_editor):
    Movie = apps.get_model('bibok', 'Movie')
    for title, year, genre, poster in MOVIES:
        Movie.objects.get_or_create(title=title, defaults={'year': year, 'genre': genre, 'poster': poster})


class Migration(migrations.Migration):
    dependencies = [('bibok', '0001_initial')]
    operations = [migrations.RunPython(add_movies, migrations.RunPython.noop)]
