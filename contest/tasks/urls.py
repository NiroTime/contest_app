from django.conf.urls.static import static
from django.urls import path

from .views import *

app_name = 'tasks'

urlpatterns = [
    path('', index, name='index'),
    path('tasks/all/', all_tasks_page, name='tasks_all'),
    path('tasks/<slug:slug>/', task_page, name='task'),
    path('profile/<username>/', profile, name='profile'),
    path('profile/<username>/edit/', profile_edit, name='profile_edit'),
    path("profile/<str:username>/follow/", profile_follow,
         name="profile_follow"),
    path("profile/<str:username>/unfollow/", profile_unfollow,
         name="profile_unfollow"),
    path('tasks/<slug:slug>/talks/', task_talks, name='task_talks'),
    path(
        'tasks/<slug:slug>/talks/comment/<int:pk>/like/',
        comment_like,
        name='comment_like'
    ),
    path(
        'tasks/<slug:slug>/talks/comment/<int:pk>/unlike/',
        comment_unlike,
        name='comment_unlike'
    ),
]
