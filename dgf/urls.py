from django.urls import path

from . import views

app_name = 'dgf'
urlpatterns = [
    path('', views.IndexView.as_view(), name='friend_index'),
    path('profile/', views.UpdateView.as_view(), name='friend_update'),
    path('feedback/', views.FeedbackCreate.as_view(), name='feedback'),
    path('media/', views.MediaIndex.as_view(), name='media'),
    path('tournaments/', views.TournamentsView.as_view(), name='tournament_index'),
    path('tournaments/<int:tournament_id>/attendance', views.attendance, name='tournament_attendance'),
    path('tremonia-series-hall-of-fame/', views.TremoniaSeriesHallOfFame.as_view(),
         name='tremonia_series_hall_of_fame'),
    path('<str:slug>/', views.DetailView.as_view(), name='friend_detail'),
]
