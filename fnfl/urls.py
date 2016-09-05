from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.lineup_list, name='lineup_list'),
    url(r'^lineup/(?P<pk>\d+)/$', views.lineup_detail, name='lineup_detail'),
    url(r'^lineup/new/$', views.lineup_new, name='lineup_new'),
    url(r'^lineup/(?P<pk>\d+)/edit/$', views.lineup_edit, name='lineup_edit'),
]
