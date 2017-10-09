from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import PermissionDenied

from .models import Tournament, Round
from .util import get_timeout


@receiver(pre_save, sender=User)
def registration_user(sender, instance, **kwargs):
    if instance.pk is None and not instance.is_staff and Round.get_current().is_last:
        raise PermissionDenied


@receiver(post_save, sender=Tournament)
def cache_current_tournament(sender, instance, created, **kwargs):
    cache.set('current_tournament', Tournament.get_current(), get_timeout(instance.end_time))


@receiver(post_save, sender=Round)
def cache_current_round(sender, instance, **kwargs):
    cache.set('current_round', Round.get_current(), get_timeout(instance.end_time))
