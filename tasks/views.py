from datetime import datetime

from django.http import Http404
from django.shortcuts import render

from .models import Task, Tournament, Round

def tournament(request):
    tournament = get_current_tournament()
    rounds = tournament.round_set.all()
    print(rounds)

    return render(request, 'tasks/tournament.html', {
            'title': tournament.title, 
            'tour_title': tournament.title, 
            'menu': 'tournament', 
            'tournament': tournament, 
            'rounds': rounds,
        }
    )

def get_current_tournament():
    now = datetime.utcnow()
    try:
        return Tournament.objects.filter(is_current=True).get()
    except Tournament.DoesNotExist:
        raise Http404
