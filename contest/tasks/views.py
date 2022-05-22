from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView

from .models import Task
from .forms import AnswerForm


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


def task_page(request, slug):
    template = 'tasks/task_detail.html'
    task = get_object_or_404(Task, slug=slug)
    form = AnswerForm(request.POST or None)
    context = {
        'form': form,
        'task': task,
    }
    if request.method == 'POST':
        f = open('tasks/task_tests/form_answer.py', 'w')
        f.write(request.POST['text'])
        f.close()
        from .task_tests.sum_a_b_c import testing
        answer = testing()
        context['answer'] = answer

    return render(request, template, context=context)
