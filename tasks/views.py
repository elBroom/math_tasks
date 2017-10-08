from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from .models import Answer, Task, Rating
from .forms import TaskForm


@login_required()
def tasks(request):
    params = {
        'title': 'Tasks',
        'menu': 'tasks',
        'can_answer': can_answer(request),
        'tasks': Task.objects.filter(rounds=request.round)
    }

    if params['can_answer']:
        params['form'] = TaskForm()
        answers = {}
        for answer in Answer.objects.filter(author=request.user.id).filter(task__in=params['tasks']):
            if answers.get(answer.task_id):
                answers[answer.task_id].append(answer)
            else:
                answers[answer.task_id] = [answer]
        params['answers'] = answers

    return render(request, 'tasks/tasks.html', params)


def rating(request):
    rating = Rating.objects.filter(round=request.round)

    return render(request, 'tasks/rating.html', {
            'title': 'Rating',
            'menu': 'rating',
            'rating': rating,
        }
    )


def tournament(request):
    rounds = request.tournament.round_set.all()

    return render(request, 'tasks/tournament.html', {
            'title': request.tournament.title,
            'menu': 'tournament',
            'rounds': rounds,
        }
    )


@require_http_methods(["POST"])
def answer(request, task_id):
    form = TaskForm(request.POST)
    if not form.is_valid():
        return HttpResponse("Error")

    task = get_object_or_404(Task, pk=task_id)
    Answer(
        author=User.objects.filter(pk=request.user.id).get(),
        task=task,
        value=form.data.get('answer')
    ).save()
    return redirect('/tasks/')


def can_answer(request):
    return not request.user.is_staff or request.user.has_perm('tasks.can_answer')
