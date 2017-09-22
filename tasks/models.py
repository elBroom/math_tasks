from django.db import models


class TimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tournament(TimeMixin):
    title = models.CharField(max_length=200)


class Round(TimeMixin):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    is_last = models.BooleanField(default=False)
    tournament = models.ForeignKey(Tournament)


class Task(TimeMixin):
    creator = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    correct_answer = models.CharField(max_length=20)
    rounds = models.ManyToManyField(Round)

    def __str__(self):
        return self.title


class Answer(TimeMixin):
    author = models.ForeignKey('auth.User')
    value = models.CharField(max_length=20)
    task = models.ForeignKey(Task)

    def __str__(self):
        return self.value


class Rating(models.Model):
    user = models.ForeignKey('auth.User')
    round = models.ForeignKey(Round)
    points = models.DecimalField(max_digits=5, decimal_places=2)
