from django.urls import path

from .views import *

app_name = 'tasks'

urlpatterns = [
    path('', index, name='index'),
    path('tasks/all/', AllTasksPage.as_view(), name='tasks_all'),
    path('tasks/<slug:slug>/', task_page, name='task'),
    path('profile/<username>', profile, name='profile'),
    path("profile/<str:username>/follow/", profile_follow,
         name="profile_follow"),
    path("profile/<str:username>/unfollow/", profile_unfollow,
         name="profile_unfollow"),
    path('tasks/<slug:slug>/talks', task_talks, name='task_talks')
]
