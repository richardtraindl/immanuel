from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /kate/5/match/
    url(r'^(?P<match_id>[0-9]+)/match/$', views.match, name='match'),
    url(r'^(?P<match_id>[0-9]+)/(?P<switch>\w+)/match/$', views.match, name='match'),
    url(r'^(?P<match_id>[0-9]+)/domove/$', views.do_move, name='domove'),
    url(r'^(?P<match_id>[0-9]+)/(?P<switch>\w+)/undomove/$', views.undo_move, name='undomove'),
    url(r'^new/$', views.new, name='new'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<match_id>[0-9]+)/addcomment/$', views.add_comment, name='addcomment'),
    url(r'^fetchcomments/$', views.fetch_comments, name='fetchcomments'),
    url(r'^fetchboard/$', views.fetch_board, name='fetchboard'),
]
