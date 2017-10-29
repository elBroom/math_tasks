from django.core.cache import cache
from django.http import Http404
from .models import Tournament, Round

from .util import get_timeout


class RoundMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/admin/') and not request.path.startswith('/summernote/'):
            request.tournament = get_current_tournament()
            request.round = get_current_round()
        return self.get_response(request)


def get_current_tournament():
    data = cache.get('current_tournament')
    if not data:
        try:
            data = Tournament.get_current()
        except Tournament.DoesNotExist:
            raise Http404
        timeout = get_timeout(data.end_time) if get_timeout(data.end_time) > 0 else 60
        cache.set('current_tournament', data, timeout)
    return data


def get_current_round():
    data = cache.get('current_round')
    if not data:
        try:
            data = Round.get_current()
        except (Round.DoesNotExist, Tournament.DoesNotExist):
            raise Http404
        timeout = get_timeout(data.end_time) if get_timeout(data.end_time) > 0 else 60
        cache.set('current_round', data, timeout)
    return data
