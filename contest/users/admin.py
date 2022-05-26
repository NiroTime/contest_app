from django.contrib import admin

from .models import Profile, UserActions


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'rating',)


class UserActionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'action_url')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserActions, UserActionsAdmin)
