from importlib import import_module

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Exists, OuterRef
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from users.forms import ProfileForm, UpdateUserForm
from users.models import UserActions, Profile, UsersSolvedTasks

from .forms import AnswerForm, CommentForm
from .models import Comment, Follow, Like, Task

User = get_user_model()


def index(request):
    template = 'tasks/index.html'
    top_users = Profile.objects.all(
    ).order_by(
        '-rating'
    )[:settings.TOP_RANK_PLAYERS_LIMIT].select_related('user')

    context = {
        'top_users': top_users,
        'title': 'Контест апп'
    }
    if request.user.is_authenticated:
        user = request.user
        following = user.following.all().select_related(
            'author'
        ).prefetch_related('author__actions')
        context['following'] = following

    return render(request, template, context=context)


class AllTasksPage(ListView):
    model = Task
    template_name = 'tasks/tasks_all.html'
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все задания'
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
        'title': f'Задание {slug}'
    }
    if request.method == 'POST':
        f = open(f'tasks/task_tests/{request.user}_{slug}.py', 'w')
        f.write(request.POST['decision'].replace('\n', ''))
        f.close()
        module_test_name = f'tasks.task_tests.test_{slug}'
        module_test = import_module(module_test_name)
        module_solution_name = f'tasks.task_tests.{request.user}_{slug}'
        try:
            module_solution = import_module(module_solution_name)
            answer = module_test.testing(
                module_test.tests,
                module_solution.solution
            )
        except Exception as err:
            answer = err

        context['answer'] = answer
        if answer == 'Тесты пройдены!':

            user = request.user
            ust = UsersSolvedTasks.objects.filter(
                user=user).filter(task=task).first()
            if not ust:
                ust = UsersSolvedTasks(
                    user=user,
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
            action = UserActions.objects.filter(
                user=user,
                description=f'выполнил(а) задание: {slug}!',
                action_url=f'/tasks/{slug}/',
            ).first()
            if not action:
                action = UserActions(
                    user=user,
                    description=f'выполнил(а) задание: {slug}!',
                    action_url=f'/tasks/{slug}/'
                )
                action.save()

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
    comments_count = Comment.objects.filter(author=author).count()
    tasks_solved = UsersSolvedTasks.objects.filter(
        user=author, solved=True
    ).count()
    likes_count = Comment.objects.filter(
        author=author
    ).aggregate(Count("like_comment"))
    context = {
        'user': user,
        'author': author,
        'following': following,
        'posts_count': comments_count,
        'tasks_solved': tasks_solved,
        'likes_count': likes_count['like_comment__count'],
    }
    return render(request, template, context=context)


@login_required
def profile_edit(request, username):
    template = 'tasks/profile_edit.html'
    user = get_object_or_404(User, username=username)
    if request.user.username != username:
        return redirect('tasks:profile', username)
    user_form = UpdateUserForm(request.POST or None, instance=user)
    profile_form = ProfileForm(
        request.POST, request.FILES or None, instance=user.profile
    )
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
        action = UserActions(
            user=request.user,
            description=f'подписался(ась) на: {username}!',
            action_url=f'/profile/{username}/'
        )
        action.save()
    return redirect('tasks:profile', username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    is_follower = Follow.objects.filter(user=request.user, author=author)
    if is_follower.exists():
        is_follower.delete()
        action = UserActions(
            user=request.user,
            description=f'отписался(ась) от: {username}!',
            action_url=f'/profile/{username}/'
        )
        action.save()
    return redirect('tasks:profile', username)


@login_required
def post_like(request, slug, pk):
    comment = Comment.objects.get(pk=pk)
    like = Like.objects.filter(user=request.user, comment=comment)
    if not like.exists():
        Like.objects.create(user=request.user, comment=comment)
    return redirect('tasks:task_talks', slug)


@login_required
def post_unlike(request, slug, pk):
    comment = Comment.objects.get(pk=pk)
    like = Like.objects.filter(user=request.user, comment=comment)
    if like.exists():
        like.delete()
    return redirect('tasks:task_talks', slug)


@login_required
def task_talks(request, slug):
    template = 'tasks/task_talks.html'
    task = get_object_or_404(Task, slug=slug)

    comments = task.comments.all().annotate(
        count_likes=Count('like_comment')
    ).annotate(is_request_user=Exists(
        Like.objects.filter(user=request.user, comment=OuterRef('pk')))
    ).select_related('author')

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.task = task
        comment.save()
        action = UserActions(
            user=request.user,
            description=f'написал(а) комментарий к заданию: {slug}!',
            action_url=f'/tasks/{slug}/talks/'
        )
        action.save()
        return redirect('tasks:task_talks', slug)
    context = {
        'task': task,
        'comments': comments,
        'form': form,
    }
    return render(request, template, context=context)
