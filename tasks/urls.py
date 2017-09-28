from django.conf.urls import url

from tasks import views

urlpatterns = [
    url(r'^$', views.tournament, name='index'),
]