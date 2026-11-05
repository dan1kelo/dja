from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('game/guess/', views.guess, name='guess'),
    path('game/next/', views.next_movie, name='next'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(extra_context={'title': 'Вход'}), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
