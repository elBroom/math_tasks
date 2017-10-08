from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.tournament, name='index'),
    url(r'^tasks/$', views.tasks, name='tasks'),
    url(r'^rating/$', views.rating, name='rating'),
    url(r'^answer/(?P<task_id>\d+)/$', views.answer, name='answer'),
]
