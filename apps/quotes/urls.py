from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^quotes$', views.quotes),
    url(r'^create$', views.create),
    url(r'^likes/(?P<quote_id>\d+)$', views.likes),
    url(r'^remove/(?P<quote_id>\d+)$', views.remove),
    url(r'^users/(?P<user_id>\d+)$', views.users),
    url(r'^dashboard$', views.dashboard),
]