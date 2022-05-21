from django.contrib import admin

from .models import Task, Category


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'slug',
        'category',
        'content',
        'is_published',
    )
    search_fields = ('content',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    list_filter = ('title',)


admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
