from django import forms
from .models import Other_applications
from django.forms import ModelForm, Textarea


class AnswerForm(ModelForm):
    class Meta:
        model = Other_applications
        fields = ['answer']
        labels = {
            'answer': (''),
        }
        widgets = {
            'answer': Textarea(attrs={'cols': 80, 'rows': 10}),
        }