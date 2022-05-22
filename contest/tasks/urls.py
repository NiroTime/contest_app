from django.urls import path

from .views import *

app_name = 'tasks'

urlpatterns = [
    path('', index, name='index'),
    path('tasks/all/', AllTasksPage.as_view(), name='tasks_all'),
    path('tasks/<slug:slug>/', task_page, name='task'),
]
