from django.urls import path

from . import views

app_name = 'dgf'
urlpatterns = [
    path('', views.IndexView.as_view(), name='friend_index'),
    path('<str:slug>/', views.DetailView.as_view(), name='friend_detail'),
]
