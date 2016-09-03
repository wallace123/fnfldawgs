from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.lineup_list, name='lineup_list'),
]
