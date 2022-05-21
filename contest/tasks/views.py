from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Task


def index(request):
    template = 'tasks/index.html'
    context = {
        'title': 'title'
    }
    return render(request, template, context=context)


class AllTasksPage(ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Task.objects.filter(is_published=True)


class TaskPage(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'tasks'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
