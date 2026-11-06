from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('game/guess/', views.guess, name='guess'),
    path('game/next/', views.next_movie, name='next'),
]
