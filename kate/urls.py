from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/(?P<matchid>\w+)/$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^create/$', views.create, name='create'),
    url(r'^load/$', views.load, name='load'),
    url(r'^move/(?P<matchid>[0-9]+)/$', views.move, name='move'),
    url(r'^undomove/(?P<matchid>\w+)/$', views.undo_move, name='undomove'),
    url(r'^addcomment/$', views.add_comment, name='addcomment'),
    url(r'^retrievecomments/$', views.retrieve_comments, name='retrievecomments'),
]
