from django import forms

from .models import Task

class TaskForm(forms.Form):
    answer = forms.CharField(max_length=100, required=True)
