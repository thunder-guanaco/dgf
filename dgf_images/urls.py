from django.urls import path

from . import views

app_name = 'dgf_images'
urlpatterns = [
    path('call', views.call, name='call'),
    path('', views.index, name='index'),
    path('<str:slug>', views.generator, name='generator'),
]
