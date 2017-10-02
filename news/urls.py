from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^news/$', views.list, name='index'),
    url(r'^news/(?P<item_id>\d+)/$', views.item, name='item'),
]