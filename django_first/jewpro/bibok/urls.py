from django.urls import path
from django.views import views

urlpatterns = [
    path('main.html', views.book_list, name='main website'),
]