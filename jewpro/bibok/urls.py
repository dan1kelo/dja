from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('game/guess/', views.guess, name='guess'),
    path('game/hint/', views.hint, name='hint'),
    path('game/restart/', views.restart, name='restart'),
    path('game/next/', views.next, name='next'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
