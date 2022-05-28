from django.contrib import admin

from .models import Profile, UserActions, UsersSolvedTasks


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'rating',)


@admin.register(UserActions)
class UserActionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'action_url')


@admin.register(UsersSolvedTasks)
class UsersSolvedTasksAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'solved', 'decision')
