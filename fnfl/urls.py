from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.welcome, name= 'welcome'),
    url(r'^lineup/$', views.lineup_list, name='lineup_list'),
    url(r'^lineup/(?P<pk>\d+)/$', views.lineup_detail, name='lineup_detail'),
    url(r'^lineup/new/$', views.lineup_new, name='lineup_new'),
    url(r'^lineup/(?P<pk>\d+)/edit/$', views.lineup_edit, name='lineup_edit'),
    url(r'^drafts/$', views.lineup_draft_list, name='lineup_draft_list'),
    url(r'^lineup/(?P<pk>\d+)/publish/$', views.lineup_publish, name='lineup_publish'),
    url(r'^lineup/(?P<pk>\d+)/remove/$', views.lineup_remove, name='lineup_remove'),
    url(r'^lineup/(?P<pk>\d+)/player/$', views.add_player, name='add_player'),
]
