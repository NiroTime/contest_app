from django.shortcuts import render, get_object_or_404
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
    template_name = 'tasks/tasks_all.html'
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Task.objects.filter(is_published=True)


def task_page(request, slug):
    template = 'tasks/task_detail.html'
    task = get_object_or_404(Task, slug=slug)
    form = AnswerForm(
        request.POST or None,
        initial={'decision': task.function_name}
    )
    context = {
        'form': form,
        'task': task,
    }
    if request.method == 'POST':
        f = open('tasks/task_tests/form_answer.py', 'w')
        f.write(request.POST['decision'])
        # как убрать лишний пропуск строки в записанном файле, и нужно ли?
        f.close()
        from .task_tests.sum_a_b_c import testing
        # как заменить sum_a_b_c на слаг из реквеста?
        answer = testing()
        context['answer'] = answer

    return render(request, template, context=context)
    # как применить что-то вроде ревёрс лейзи, чтобы небыло затупов при рендере
