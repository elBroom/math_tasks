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
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    class Meta:
        index_together = (('start_time', 'end_time'),)

    def __str__(self):
        return self.title


class Round(TimeMixin):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    is_last = models.BooleanField(default=False)
    tournament = models.ForeignKey(Tournament)

    class Meta:
        index_together = (('start_time', 'end_time'),)

    def __str__(self):
        return self.title

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


class Task(TimeMixin):
    creator = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    correct_answer = models.CharField(max_length=20)
    rounds = models.ManyToManyField(Round)

    class Meta:
        index_together = (('id', 'correct_answer'),)

    def __str__(self):
        return self.title


class Answer(TimeMixin):
    author = models.ForeignKey('auth.User')
    value = models.CharField(max_length=20)
    task = models.ForeignKey(Task)
    is_success = models.NullBooleanField()

    def __str__(self):
        return self.value

    def save(self, *args, **kwargs):
        self.value = prepare_answer(self.value)
        self.is_success = Task.objects.filter(id=self.task.id).filter(correct_answer=self.value).exists()
        super(Answer, self).save(*args, **kwargs)


class Rating(models.Model):
    user = models.ForeignKey('auth.User')
    round = models.ForeignKey(Round)
    points = models.DecimalField(max_digits=5, decimal_places=2)
