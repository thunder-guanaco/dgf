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
    path('bag-tags/<int:bag_tag>/claim', views.bag_tag_claim, name='bag_tag_claim'),
    path('bag-tags/new', views.bag_tag_new, name='bag_tag_new'),
    path('bag-tags/', views.bag_tag_update, name='bag_tag_update'),
    path('tremonia-series/next-tournament', views.ts_next_tournament, name='tremonia_series_next_tournament'),
    path('tremonia-series/future-dates', views.ts_future_dates, name='tremonia_series_future_dates'),
    path('<str:slug>/', views.DetailView.as_view(), name='friend_detail'),
]
