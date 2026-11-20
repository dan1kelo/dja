from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Movie, Profile


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'genre')
    search_fields = ('title',)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


admin.site.unregister(User)


@admin.register(User)
class PlayerAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ('id', 'username', 'email', 'score', 'is_staff')
    list_display_links = ('id', 'username')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile')

    @admin.display(description='Score', ordering='profile__score')
    def score(self, obj):
        return obj.profile.score if hasattr(obj, 'profile') else 0
