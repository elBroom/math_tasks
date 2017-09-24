from django.db import transaction
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Task, Tournament, Round
from .util import prepare_answer


class TournamentAdmin(admin.ModelAdmin):
    readonly_fields = ('start_time', 'end_time')


class RoundAdmin(admin.ModelAdmin):
    @transaction.atomic
    def save_model(self, request, obj, form, change):
        super(RoundAdmin, self).save_model(request, obj, form, change)

        start_time = obj.start_time
        end_time = obj.end_time
        for round in Round.objects.all().filter(tournament=obj.tournament):
            if round.id != obj.id:
                start_time = min(start_time, round.start_time)
                end_time = max(end_time, round.end_time)

        if obj.tournament.start_time != start_time or obj.tournament.end_time != obj.end_time:
            obj.tournament.start_time = start_time
            obj.tournament.end_time = obj.end_time
            obj.tournament.save()


class TaskAdmin(SummernoteModelAdmin):
    exclude = ('creator',)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.correct_answer = prepare_answer(obj.correct_answer)
        super(TaskAdmin, self).save_model(request, obj, form, change)


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Task, TaskAdmin)
