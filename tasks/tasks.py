from django.contrib.auth.models import Permission, User
from django.db import transaction
from django.db.models import Min, Count
from celery.utils.log import get_task_logger

from math_tasks import settings
from math_tasks.celery import app
from .models import Answer, Round, Rating
from .util import get_delta_minute

logger = get_task_logger(__name__)


@app.task(bind=True, ignore_result=True)
@transaction.atomic
def calculate_rating_task(self, round_id):
    logger.info('Start calculate_rating_task with key'.format(round_id))
    try:
        round = Round.objects.filter(pk=round_id).get()
    except Round.DoesNotExist:
        logger.info('Round with key {} not found'.format(round_id))
        return

    answers = Answer.objects.values('author_id', 'task_id', 'is_success') \
        .annotate(time=Min('created_at'), count=Count('task_id')) \
        .filter(task__in=round.tasks.all())

    users = {}
    for answer in answers:
        user = users.get(answer['author_id'], {})
        points = get_delta_minute(round.start_time, answer['time']) if answer['is_success'] else \
            answer['count'] * get_delta_minute(round.start_time, round.end_time)
        if user:
            user['points'] += points
        else:
            user['user_id'] = answer['author_id']
            user['points'] = points
        users[answer['author_id']] = user

    rating_dict = {rating.user_id: rating for rating in Rating.objects.filter(round=round)}
    for user in users.values():
        rating = rating_dict.get(user['user_id'], Rating(user_id=user['user_id'], round=round))
        rating.points = user['points']
        rating.save()

    change_permission_task.delay(round_id)
    logger.info('Finish calculate_rating_task with key'.format(round_id))


@app.task(bind=True, ignore_result=True)
@transaction.atomic
def change_permission_task(self, round_id):
    logger.info('Start change_permission_task with key'.format(round_id))
    try:
        round = Round.objects.filter(pk=round_id).get()
    except Round.DoesNotExist:
        logger.info('Round with key {} not found'.format(round_id))
        return

    top = set()
    for round in Round.objects.filter(tournament=round.tournament):
        top |= set([rating.user_id for rating in
                    Rating.objects.filter(round=round).all()[:settings.TASKS_FINAL_USERS_LIMIT]])

    permission = Permission.objects.get(codename='can_create_answer')
    for user in User.objects.filter(is_staff=False).filter(is_active=True):
        if user.id in top:
            user.user_permissions.add(permission)
        else:
            user.user_permissions.remove(permission)
        user.save()

    logger.info('Finish change_permission_task with key'.format(round_id))
