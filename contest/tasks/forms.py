from django import forms


class AnswerForm(forms.Form):
    decision = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 45, 'rows': 35})
    )
