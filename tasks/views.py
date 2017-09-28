from django.utils import timezone

from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Answer, Task, Tournament, Rating
from .forms import TaskForm


def tasks(request):
    tournament = get_current_tournament()
    round = get_current_round()
    tasks = Task.objects.filter(rounds=round)
    form = TaskForm()

    return render(request, 'tasks/tasks.html', {
            'title': 'Tasks',
            'tour_title': tournament.title,
            'menu': 'tasks',
            'tasks': tasks,
            'form': form,
        }
    )


def rating(request):
    tournament = get_current_tournament()
    round = get_current_round()
    rating = Rating.objects.filter(round=round).order_by('-points')

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

    try:
        task = Task.objects.filter(pk=task_id).get()
    except Task.DoesNotExist:
        raise Http404

    answer = Answer()
    answer.author = User.objects.filter(pk=1).get()
    answer.task = task
    answer.value = form.data.get('answer')
    answer.save()
    return HttpResponse("OK")


def get_current_tournament():
    try:
        return Tournament.objects.filter(is_current=True).get()
    except Tournament.DoesNotExist:
        raise Http404


def get_current_round():
    now = timezone.now()
    tournament = get_current_tournament()

    for round in sorted(tournament.round_set.all(), key=lambda x: x.start_time):
        if round.start_time > now and round.end_time > now:
            return round
        if round.start_time >= now and round.end_time <= now:
            return round
        if round.is_last:
            return round