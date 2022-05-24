from django import forms
from django.forms import ModelForm

from .models import Comment, Follow


class AnswerForm(forms.Form):
    decision = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 45, 'rows': 35})
    )


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Добавить комментарий'}
        help_texts = {'text': 'Текст комментария'}


class FollowForm(ModelForm):
    class Meta:
        model = Follow
        labels = {'user': 'Подписка на:', 'author': 'Автор записи'}
        fields = ['user']
