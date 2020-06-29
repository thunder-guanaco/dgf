from django.urls import path

from . import views

app_name = 'dgf'
urlpatterns = [
    path('', views.IndexView.as_view(), name='friend_index'),
    path('profile/', views.UpdateView.as_view(), name='friend_update'),
    path('feedback/', views.FeedbackCreate.as_view(), name='feedback'),
    path('media/', views.MediaIndex.as_view(), name='media'),
    path('tournaments/', views.TournamentsView.as_view(), name='tournaments_index'),
    path('tournaments/attend/', views.AttendanceCreate.as_view(), name='tournament_attend'),
    path('tournaments/withdraw/<int:pk>', views.AttendanceDelete.as_view(), name='tournament_withdraw'),
    path('success/', views.success, name='success'),
    path('<str:slug>/', views.DetailView.as_view(), name='friend_detail'),
]
