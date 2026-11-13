from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('game/guess/', views.guess, name='guess'),
    path('game/hint/', views.hint, name='hint'),
    path('game/skip/', views.skip, name='skip'),
    path('game/restart/', views.restart, name='restart'),
]
