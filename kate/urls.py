from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<matchid>[0-9]+)/match/$', views.match, name='match'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>[0-1])/match/$', views.match, name='match'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>[0-1])/(?P<msg>[0-9]+)/match/$', views.match, name='match'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>[0-1])/domove/$', views.do_move, name='domove'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>[0-1])/undomove/$', views.undo_move, name='undomove'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>[0-1])/resume/$', views.resume, name='resume'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^(?P<switch>[0-1])/settings/$', views.settings, name='settings'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>[0-1])/settings/$', views.settings, name='settings'),
    url(r'^(?P<matchid>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<matchid>[0-9]+)/addcomment/$', views.add_comment, name='addcomment'),
    url(r'^fetchcomments/$', views.fetch_comments, name='fetchcomments'),
    url(r'^fetchmatch/$', views.fetch_match, name='fetchmatch'),
]
