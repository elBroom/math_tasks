from django.utils import timezone

from django.core.exceptions import ValidationError
from django.db import models

from .util import prepare_answer


class TimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tournament(TimeMixin):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ('id',)
        index_together = (('start_time', 'end_time'),)

    def __str__(self):
        return self.title

    @classmethod
    def get_current(cls):
        return cls.objects.filter(is_current=True).get()


class Round(TimeMixin):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    is_last = models.BooleanField(default=False)
    tournament = models.ForeignKey(Tournament)

    class Meta:
        ordering = ('id',)
        index_together = (('start_time', 'end_time'),)

    def __str__(self):
        return '{}/{}'.format(self.tournament.title, self.title)

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Times are incorrect")

        # One round in moment
        round = Round.objects.exclude(id=self.id).filter(
                models.Q(start_time__range=(self.start_time, self.end_time)) |
                models.Q(end_time__range=(self.start_time, self.end_time))
            )
        if round.exists():
            raise ValidationError("One round in moment")

    @classmethod
    def get_current(cls):
        now = timezone.now()
        tournament = Tournament.get_current()
        for round in sorted(tournament.round_set.all(), key=lambda x: x.start_time):
            if round.start_time > now and round.end_time > now:
                return round
            if round.start_time <= now and round.end_time >= now:
                return round
            if round.is_last:
                return round


class Task(TimeMixin):
    creator = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    correct_answer = models.CharField(max_length=20)
    rounds = models.ManyToManyField(Round, related_name="tasks")

    class Meta:
        ordering = ('id',)
        index_together = (('id', 'correct_answer'),)

    def __str__(self):
        return self.title


class Answer(TimeMixin):
    author = models.ForeignKey('auth.User')
    value = models.CharField(max_length=20)
    task = models.ForeignKey(Task)
    is_success = models.NullBooleanField()

    class Meta:
        permissions = (
            ("can_create_answer", "Can create answer"),
        )

    def __str__(self):
        return self.value

    def save(self, *args, **kwargs):
        self.value = prepare_answer(self.value)
        self.is_success = Task.objects.filter(id=self.task.id).filter(correct_answer=self.value).exists()
        super(Answer, self).save(*args, **kwargs)


class Rating(models.Model):
    user = models.ForeignKey('auth.User')
    round = models.ForeignKey(Round)
    points = models.IntegerField()

    class Meta:
        ordering = ('points',)


from .signals import *
