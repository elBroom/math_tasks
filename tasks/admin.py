from django.contrib import admin

from .models import Answer, Task, Tournament, Round

admin.site.register(Tournament)
admin.site.register(Round)
admin.site.register(Task)
admin.site.register(Answer)
