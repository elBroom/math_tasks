from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from .models import Answer, Task, Tournament, Rating, Round
from .forms import TaskForm
from .util import get_timeout


@login_required(login_url='/accounts/login/')
def tasks(request):
    tournament = get_current_tournament()
    round = get_current_round()
    tasks = Task.objects.filter(rounds=round)
    form = TaskForm()

    answers = {}
    for answer in Answer.objects.filter(author=request.user.id).filter(task__in=tasks):
        if answers.get(answer.task_id):
            answers[answer.task_id].append(answer)
        else:
            answers[answer.task_id]= [answer]

    return render(request, 'tasks/tasks.html', {
            'title': 'Tasks',
            'tour_title': tournament.title,
            'menu': 'tasks',
            'tasks': tasks,
            'answers': answers,
            'form': form,
        }
    )


def rating(request):
    tournament = get_current_tournament()
    round = get_current_round()
    rating = Rating.objects.filter(round=round)

    return render(request, 'tasks/rating.html', {
            'title': 'Rating',
            'tour_title': tournament.title,
            'menu': 'rating',
            'rating': rating,
        }
    )


def tournament(request):
    tournament = get_current_tournament()
    rounds = tournament.round_set.all()

    return render(request, 'tasks/tournament.html', {
            'title': tournament.title, 
            'tour_title': tournament.title, 
            'menu': 'tournament', 
            'tournament': tournament, 
            'rounds': rounds,
        }
    )


@require_http_methods(["POST"])
def answer(request, task_id):
    form = TaskForm(request.POST)
    if not form.is_valid():
        return HttpResponse("Error")

    task = get_object_or_404(Task, pk=task_id)
    answer = Answer()
    answer.author = User.objects.filter(pk=request.user.id).get()
    answer.task = task
    answer.value = form.data.get('answer')
    answer.save()
    return redirect('/tasks')


def get_current_tournament():
    data = cache.get('current_tournament')
    if not data:
        try:
            data =  Tournament.get_current()
        except Tournament.DoesNotExist:
            raise Http404
        timeout = get_timeout(data.end_time) if get_timeout(data.end_time) > 0 else 60
        cache.set('current_tournament', data, timeout)
    return data


def get_current_round():
    data = cache.get('current_round')
    if not data:
        data = Round.get_current()
        timeout = get_timeout(data.end_time) if get_timeout(data.end_time) > 0 else 60
        cache.set('current_round', data, timeout)
    return data
