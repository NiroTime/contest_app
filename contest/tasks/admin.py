from django.contrib import admin

from .models import Category, Flexibility, Task


@admin.register(Task)
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    list_filter = ('title',)


@admin.register(Flexibility)
class FlexibilityAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    list_filter = ('title',)


