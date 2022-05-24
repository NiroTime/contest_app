from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView

from .models import Task, Follow
from .forms import AnswerForm, CommentForm
from users.models import Profile, UsersSolvedTasks
from users.forms import ProfileForm, UpdateUserForm


User = get_user_model()


def index(request):
    template = 'tasks/index.html'
    top_users = Profile.objects.all().order_by('-rating')
    context = {
        'top_users': top_users
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


@login_required
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
        print(111)
        f = open('tasks/task_tests/form_answer.py', 'w')
        f.write(request.POST['decision'])
        # как убрать лишний пропуск строки в записанном файле, и нужно ли?
        f.close()
        print(222)
        from .task_tests.sum_a_b_c import testing
        print(333)
        # как заменить sum_a_b_c на слаг из реквеста?
        answer = testing()
        context['answer'] = answer
        if answer == 'Тесты пройдены!':

            user = request.user
            ust = UsersSolvedTasks.objects.filter(
                user=user).filter(task=task).first()
            if not ust:
                ust = UsersSolvedTasks(
                    user=request.user,
                    task=task,
                    solved=False,
                    decision=''
                )
                ust.save()
            if not ust.solved:
                user.profile.rating += task.task_rating
                ust.solved = True
            ust.decision = request.POST['decision']
            ust.save()
            user.profile.save()

    return render(request, template, context=context)
    # как применить что-то вроде ревёрс лейзи, чтобы небыло затупов при рендере


def profile(request, username):
    template = 'tasks/profile.html'
    author = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=author
        ).exists()
    else:
        following = False
    user = request.user
    context = {
        'user': user,
        'author': author,
        'following': following,
    }
    return render(request, template, context=context)


@login_required
def profile_edit(request, username):
    template = 'tasks/profile_edit.html'
    user = get_object_or_404(User, username=username)
    if request.user.username != username:
        return redirect('users:profile', username)
    user_form = UpdateUserForm(request.POST, instance=user)
    profile_form = ProfileForm(request.POST, instance=user.profile)
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return redirect('tasks:profile', username)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, template, context=context)


@login_required
def profile_follow(request, username):
    user = request.user
    author = User.objects.get(username=username)
    is_follower = Follow.objects.filter(user=user, author=author)
    if user != author and not is_follower.exists():
        Follow.objects.create(user=user, author=author)
    return redirect('tasks:profile', username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    is_follower = Follow.objects.filter(user=request.user, author=author)
    if is_follower.exists():
        is_follower.delete()
    return redirect('tasks:profile', username)


# @login_required
# def add_comment(request, username, post_id):
#     post = get_object_or_404(Task, id=post_id, author__username=username)
#     form = CommentForm(request.POST or None)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.author = request.user
#         comment.post = post
#         comment.save()
#         return redirect('post', username, post_id)
#     return render(request, 'includes/comments.html', {'form': form,
#                   'post': post})
