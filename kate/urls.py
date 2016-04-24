from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /kate/5/match/
    url(r'^(?P<matchid>[0-9]+)/match/$', views.match, name='match'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>[0-1])/match/$', views.match, name='match'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>[0-1])/(?P<markmove>[0-1])/match/$', views.match, name='match'),
    url(r'^(?P<matchid>[0-9]+)/domove/$', views.do_move, name='domove'),
    url(r'^(?P<matchid>[0-9]+)/(?P<switch>\w+)/undomove/$', views.undo_move, name='undomove'),
    url(r'^new/$', views.new, name='new'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<matchid>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<matchid>[0-9]+)/update/$', views.update, name='update'),
    url(r'^(?P<matchid>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<matchid>[0-9]+)/addcomment/$', views.add_comment, name='addcomment'),
    url(r'^fetchcomments/$', views.fetch_comments, name='fetchcomments'),
    url(r'^fetchboard/$', views.fetch_board, name='fetchboard'),
]
