from django import forms


class TaskForm(forms.Form):
    answer = forms.CharField(max_length=100, required=True)
