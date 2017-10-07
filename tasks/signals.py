from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Tournament, Round
from .util import get_timeout


@receiver(post_save, sender=Tournament)
def create_user_profile(sender, instance, created, **kwargs):
    cache.set('current_tournament', Tournament.get_current(), get_timeout(instance.end_time))

@receiver(post_save, sender=Round)
def save_user_profile(sender, instance, **kwargs):
    cache.set('current_round', Round.get_current(), get_timeout(instance.end_time))