from django.urls import path

from . import views

app_name = 'dgf_league'
urlpatterns = [
    path('', views.TeamIndexView.as_view(), name='team_index'),
    path('<int:year>', views.TeamIndexView.as_view(), name='team_index_year'),
    path('friend_without_team/add', views.friend_without_team_add, name='friend_without_team_add'),
    path('teams/add', views.team_add, name='team_add'),
    path('results/add', views.result_add, name='result_add'),
]
