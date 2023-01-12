from django.urls import path

from . import views

app_name = 'dgf_league'
urlpatterns = [
    path('', views.TeamIndexView.as_view(), name='team_index'),
    path('teams/add', views.team_add, name='team_add'),
]
