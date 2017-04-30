from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<matchid>[0-9]+)/match/$', views.match, name='match'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>[0-1])/match/$', views.match, name='match'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>[0-1])/(?P<msg>[0-9]+)/match/$', views.match, name='match'),
    url(r'^(?P<matchid>[0-9]+)/domove/$', views.do_move, name='domove'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>[0-1])/forcemove/$', views.force_move, name='forcemove'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>[0-1])/undomove/$', views.undo_move, name='undomove'),
    url(r'^new/$', views.new, name='new'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>[0-1])/edit/$', views.edit, name='edit'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>[0-1])/update/$', views.update, name='update'),
    url(r'^(?P<matchid>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<matchid>[0-9]+)/addcomment/$', views.add_comment, name='addcomment'),
    url(r'^fetchcomments/$', views.fetch_comments, name='fetchcomments'),
    url(r'^fetchmatch/$', views.fetch_match, name='fetchmatch'),
]
