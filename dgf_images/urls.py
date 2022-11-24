from django.urls import path

from . import views

app_name = 'dgf'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:slug>', views.generator, name='generator'),
]
