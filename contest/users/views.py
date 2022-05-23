from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from .forms import CreationForm, ProfileForm, UpdateUserForm
from .models import User


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


def profile(request, username):
    template = 'users/profile.html'
    user = get_object_or_404(User, username=username)
    context = {
        'user': user,
    }
    return render(request, template, context=context)


@login_required
def profile_edit(request, username):
    template = 'users/profile_edit.html'
    user = get_object_or_404(User, username=username)
    if request.user.username != username:
        return redirect('users:profile', username)
    user_form = UpdateUserForm(request.POST, instance=user)
    profile_form = ProfileForm(request.POST, instance=user.profile)
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return redirect('users:profile', username)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, template, context=context)
